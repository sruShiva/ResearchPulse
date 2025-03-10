import google.generativeai as genai
import re
import os
import networkx as nx
from langchain_community.graphs import ArangoGraph
from utilities.arango_fetcher import ArangoDBFetcher

import dotenv

dotenv.load_dotenv()


db_name = os.environ['ARANGO_DB_NAME']
username = os.environ['ARANGO_USERNAME']
password =  os.environ['ARANGO_PASSWORD']
host_url = os.environ['ARANGO_HOST_URL']

arango_fetcher = ArangoDBFetcher(db_name, username, password, host_url)
graph_name = arango_fetcher.get_graph_name()
edge_definitions = arango_fetcher.get_edge_definitions()
arango_db = arango_fetcher.get_arango_db()
graph_schema= arango_fetcher.get_graph_schema()

# G_adb = nxadb.Graph(name=graph_name, db=arango_db)
G_adb = arango_fetcher.fetch_graph_data()

class ProfessorPersona:
    def __init__(self, graph_name, G_adb, schema,nx):
        self.graph_name = graph_name
        self.G_adb = G_adb
       
        self.arango_schema = schema
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.nx=nx

    def text_to_aql_to_text(self, query: str):
        """Converts a natural language query into AQL, executes it, and provides an explanation."""
        
        # Convert natural language to AQL
        aql_response = self.model.generate_content(f"""
        Please convert the following query into AQL. Only return the AQL query, and do not include any additional information. 
        Ensure the query is correct and double-check it before providing the response.
        
        WHEREVER NECESSARY: Begin the query with relevant phrases such as 'WITH Email_node'.
        
        Given Query: {query}
        
        Graph name: {self.graph_name}
        Edge Definitions: {edge_definitions}
        """)

        aql_query = aql_response.text.strip()
        print("1) Generated AQL Query:")
        print(aql_query)

        # Clean up query formatting
        aql_query = aql_query.replace('```aql', '').replace('```', '')

        # Format AQL properly
        formatted_response_aql = self.model.generate_content(f"""
        Format the given query in proper AQL syntax. Ensure it follows correct AQL formatting and remove unnecessary characters or strings.
        
        Given query: {aql_query}
        
        Graph name: {self.graph_name}
        Edge Definitions: {edge_definitions}
        """)

        formatted_aql = formatted_response_aql.text.strip().replace('```aql', '').replace('```', '')
        print("2) Formatted AQL Query:")
        print(formatted_aql)

        # Execute the query in the database
        try:
            result = arango_fetcher.query(aql_query)
            print("3) Results from Graph Database:")
            print(result)
        except Exception as e:
            print("Error executing AQL:", e)
            return f"Error executing AQL: {e}"

        # Interpret the result
        interpretation = self.model.generate_content(f"""
        Explain the answer with respect to the given graph for the question.
        Provide the answer in 20 words only.
        
        Graph properties:
        - Graph name: {self.graph_name}
        - Edge Definitions: {edge_definitions}
        
        Question: {query}
        Answer: {result}
        """)

        interpretation_text = interpretation.text.strip()
        print("4) Interpretation of Results:")
        print(interpretation_text)

        return interpretation_text
    
    def text_to_nx_algorithm_to_text(self, query):
        """This tool invokes a NetworkX algorithm on the ArangoDB Graph.

        It accepts a Natural Language Query, determines which algorithm should be used,
        executes the algorithm, and translates the results back into Natural Language.

        If the query (e.g., traversals, shortest paths, etc.) can be solved using
        the Arango Query Language (AQL), do not use this tool.
        """

     

        ######################
        print("1) Generating NetworkX code")

        text_to_nx_response = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have the following graph analysis query: {query}.

        Generate the Python Code required to answer the query using the `G_adb` object.

        Be very precise in selecting the NetworkX algorithm to answer this query. Think step by step.

        Only assume that `networkx` is installed, along with other standard Python libraries.

        Always set the last variable as `FINAL_RESULT`, which represents the answer to the original query.

        Only provide Python code that I can directly execute via `exec()`. Do not provide any instructions.
        
     
        Ensure that `FINAL_RESULT` stores a short and concise answer. Avoid setting this variable to a long sequence.

        Your code:
        """)

        text_to_nx = text_to_nx_response.text.strip()
        text_to_nx_cleaned = re.sub(r"^```python\n|```$", "", text_to_nx, flags=re.MULTILINE).strip()

        print('-'*10)
        print(text_to_nx_cleaned)
        print('-'*10)

        ######################

        print("\n2) Executing NetworkX code")
        global_vars = {"G_adb": self.G_adb, "nx": self.nx}
        local_vars = {}

        try:
            exec(text_to_nx_cleaned, global_vars, local_vars)
            text_to_nx_final = text_to_nx
        except Exception as e:
            print(f"EXEC ERROR: {e}")
            return f"EXEC ERROR: {e}"

        print('-'*10)
        FINAL_RESULT = local_vars["FINAL_RESULT"]
        print(f"FINAL_RESULT: {FINAL_RESULT}")
        print('-'*10)

        ######################

        print("3) Formulating final answer")

        nx_to_text_response = self.model.generate_content(f"""
            I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}
            
            I have the following graph analysis query: {query}.

            I have executed the following Python code to help me answer my query:

            ---
            {text_to_nx_final}
            ---

            The `FINAL_RESULT` variable is set to the following: {FINAL_RESULT}.
            Assume the graph is for 'University of oxford' and answer queries.
            Based on my original Query and `FINAL_RESULT`, generate a short and concise response
            to answer my query.

            Your response:
        """)

        return nx_to_text_response.text.strip()


   

    def query_graph(self,query):

        tools = [{"tool name" : self.text_to_aql_to_text,  "tool_description" : "This tool is available to invoke the ArangoGraphQAChain object, which enables you totranslate a Natural Language Query into AQL, execute the query, and translate the result back into Natural Language."},
            {"tool name" : self.text_to_nx_algorithm_to_text,  "tool_description" : "This tool invokes a NetworkX algorithm on the ArangoDB Graph. It accepts a Natural Language Query, determines which algorithm should be used, executes the algorithm, and translates the results back into Natural Language. If the query (e.g., traversals, shortest paths, etc.) can be solved using the Arango Query Language (AQL), do not use this tool."},
                ]
        """Processes a query using Gemini and a set of tools."""

     

        # Manually integrate tools into the prompt
        system_prompt = (
            "You have access to the following tools:\n"
            f"{tools}\n"
            f"Query is  {query}"
        "Based on the query suggest which tool should be used."
        "For simple queries you can suggest :text_to_aql_to_text "
        "For complex ones, you can suggest : text_to_nx_algorithm_to_text"

        "REMEMBER ONLY TELL THE NAME OF THE TOOL WORD TO WORD"
        )
        tool_name = self.generate_content(system_prompt).text.strip()
        print(tool_name)
        if tool_name =="text_to_aql_to_text":
            return self.text_to_aql_to_text(query)
        elif tool_name =="text_to_nx_algorithm_to_text":
            return self.text_to_nx_algorithm_to_text(query)
       
        else:
            return "No appropriate tool available at the moment"
        

    def answer_query_professor(self,query):

        try:
            answer_to_general_query = self.model.generate_content(f"""
            I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

            Assume the graph is about a large institution named University of Oxford. 
            You are free to assume data for University of Oxford beyond the graph dataa points.
            You are a research analyser who is helping professors with research opportunities from that institution.
            Your task is to answer the given query for a professors based on research opportunities in Europe.
            Provide relevant answers based on the research conditions in Europe only.
            Provide answers in an encouraging manner. Give responses within 100 words only.
            Query: {query}
            Your answer is:


            """)

            answer_to_general_query = answer_to_general_query.text.strip()
            return answer_to_general_query
        except Exception as e:
            print(f"An error occured {e}")
