import google.generativeai as genai
import re
import os
import networkx as nx
from langchain_community.graphs import ArangoGraph
from utilities.arango_fetcher import ArangoDBFetcher
from utilities.search_news import SearchNews
import dotenv
import matplotlib as plt
dotenv.load_dotenv()


db_name = os.environ['ARANGO_DB_NAME']
username = os.environ['ARANGO_USERNAME']
password =  os.environ['ARANGO_PASSWORD']
host_url = os.environ['ARANGO_HOST_URL']

arango_fetcher = ArangoDBFetcher(db_name, username, password, host_url)
search_news = SearchNews()
graph_name = arango_fetcher.get_graph_name()
edge_definitions = arango_fetcher.get_edge_definitions()
arango_db = arango_fetcher.get_arango_db()
graph_schema= arango_fetcher.get_graph_schema()

# G_adb = nxadb.Graph(name=graph_name, db=arango_db)
G_adb = arango_fetcher.fetch_graph_data()

class BenefactorPersona:
    def __init__(self, graph_name, G_adb, schema,nx):
        self.graph_name = graph_name
        self.G_adb = G_adb
       
        self.arango_schema = schema
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.nx=nx

    def analyse_networkx(self,query):
        """
    This tool applies a NetworkX algorithm to the ArangoDB graph based on a natural language query.

    It processes the query to identify the most appropriate algorithm, executes the necessary computations, and then converts the results into a clear, human-readable explanation.

    The tool analyzes the problem, selects the most suitable function, and interprets the output to provide insightful explanations.
        """

   

    ######################
        print("1) Understanding requirement")

        understanding_requirement = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have the following graph analysis query: {query}.

        The following algorithms are supported by my backend (nx-cugraph):
        - Centrality: Betweenness Centrality, Degree Centrality, Eigenvector Centrality, Katz Centrality
        - Clustering: Average Clustering, Clustering Coefficients, Transitivity, Triangles
        - Community Detection: Louvain Communities (via `louvain_communities`)
        - Components: Connected Components, Weakly Connected Components
        - Core Analysis: Core Number, K-Truss
        - Link Analysis: PageRank, HITS
        - Shortest Paths: Dijkstra's Algorithm, Bellman-Ford Algorithm, Breadth-First Search
        - Tree Recognition: Is Tree, Is Forest

        Based on the query and the graph schema, suggest the most suitable measures or algorithms from the list above to analyze the graph.
       
        DO NOT suggest algorithms or methods outside of this list. For example:
        - Avoid suggesting unsupported methods like `greedy_modularity_communities` or `best_partition`.
        - Focus on algorithms that leverage GPU acceleration and are compatible with nx-cugraph.

        PROVIDE ONLY THE NAME OF THE MEASURES BY A COMMA-SEPARATED STRING. DO NOT PROVIDE ANY ADDITIONAL DATA.
        Your most suitable recommended measure:
        """)


        requirement = understanding_requirement.text.strip()


        print('-'*10)
        print(requirement)
        print('-'*10)


        ######################

        print("\n2) Creating code according to requirement")
        global_vars = {"G_adb": G_adb, "nx": nx}
        local_vars = {}

        code_for_analysis = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have the following graph analysis query: {requirement}.

        Generate the Python Code required to answer the query using the `G_adb` object.

        Be very precise in selecting the NetworkX algorithm to answer this query. Think step by step.

        IMPORTANT: IF NEEDED use NetworkX's built-in `louvain_communities` function from `networkx.algorithms.community` instead of `community.best_partition`. Do not import or use the `community` module at all.
        Avoid generating a range of values, rather filter only relebvant values. If there are a range of vlaues. truncate it to only 5-6 values.
        Always set the last variable as `FINAL_RESULT`, which represents the answer to the original query.

        Only provide Python code that I can directly execute via `exec()`. Do not provide any instructions or comments.

        Ensure that `FINAL_RESULT` stores a short and concise answer. Avoid setting this variable to a long sequence.

        Your code:
        """)


        code_to_analyse = code_for_analysis.text.strip()

        code_to_analyse_cleaned = re.sub(r"^```python\n|```$", "", code_to_analyse, flags=re.MULTILINE).strip()

        print('-'*10)
        print(code_to_analyse_cleaned)
        print('-'*10)

        ######################

        print("\n2) Executing NetworkX code")
        global_vars = {"G_adb": G_adb, "nx": nx}
        local_vars = {}

        try:
            exec(code_to_analyse_cleaned, global_vars, local_vars)
            text_to_nx_final = code_to_analyse_cleaned
        except Exception as e:
            print(f"EXEC ERROR: {e}")
            return f"EXEC ERROR: {e}"

        print('-'*10)
        FINAL_RESULT = local_vars["FINAL_RESULT"]
        print(f"FINAL_RESULT: {FINAL_RESULT}")
        print('-'*10)

        # #####################

        search_info = search_news.fetch_top_news(query)

        print('-'*10)
        print(search_info)
        print('-'*10)

        print("3) Formulating final answer")

        nx_to_text_response = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        My graph analysis query is:
        {query}

        Additionally, here are the top 3 latest relevant news articles from Europe to provide context:
        {search_info}

        I executed the following Python code to analyze my query:

        ---
        {code_to_analyse_cleaned}
        ---

        The `FINAL_RESULT` variable is set to: {FINAL_RESULT}.

        Considering my original Query, `FINAL_RESULT`, and the recent European news context provided above, generate a short and concise response. Clearly state the analysis result in simple BUSINESS TERMS ONLY. Provide stakeholders with actionable insights and useful information gained from both the analysis and recent news context.
        
        Your response:
        """)


        return nx_to_text_response.text.strip()



    def visualize_graph(self,query):
        """
        This tool applies a NetworkX algorithm to the graph based on a natural language query.

        It processes the query to identify the most appropriate algorithm, executes the necessary computations, 
        and converts the results into a clear, human-readable explanation with a relevant visualization.

        The tool analyzes the problem, selects the best function, and interprets the output to provide insightful explanations.
        """

        # Assuming you have a Generative model instance (e.g., `genai.GenerativeModel`)
       

        ######################
        print("1) Understanding the requirement")

        understanding_requirement = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have the following graph analysis query: {query}.

        Understand the requirement and suggest the most suitable plot to visualize the analysis.

        PROVIDE A 20 WORD DESCRIPTION FOR THE MOST SUITABLE PLOT TO VISUALIZE THE GRAPH.
        REMEMBER IT IS A NETWORK X PLOT. MAKE SURE THE DESCRIPTION IS RELEVANT.
        Your most suitable plot is:
        """)

        plot_requirement = understanding_requirement.text.strip()

        print('-' * 10)
        print(plot_requirement)
        print('-' * 10)

        ######################

        print("\n2) Creating code according to requirement")


        code_for_analysis = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have the following graph analysis query: {plot_requirement}.

        Generate the Python Code required to answer the query using the `G_adb` object.

        Be very precise in selecting the NetworkX algorithm to answer this query. Think step by step.

        ### **Fix Common Errors:**
        1. **Always import the required libraries**:
        - `import numpy as np`
        - `import networkx as nx`
        - `import matplotlib.pyplot as plt`
        2. **Ensure `np` is defined before use** to avoid execution errors.
        3. **Check if the graph (`G_adb`) is empty** before computing the adjacency matrix.
        4. **If the adjacency matrix is empty, return `"No connections found in the graph."`**
        5. **Ensure `plt.show()` is always executed** to display the visualization.

        Your Python code:
        """)



        code_to_analyse = code_for_analysis.text.strip()

        code_for_analysis_check = self.model.generate_content(f"""
        I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

        I have a code for a given query:
        Query:{query}
        Code : {code_to_analyse}

        Make sure the code is relevant to the graph and contains all nodes suitable for the plot.
        Ensure the code is syntactically correct and runs properly.
        ONLY relevant values based on the given schema should be present. Remove any uncessary data.
        Remove any library and it's definition apart from matplotlib and
        REMEMBER: I have to make a plot, make sure to provide the code for a graph.
        REMEMBER: IT IS A NETWORK X PLOT. MAKE SURE THE CODE IS ABLE TO PLOT A NETWORK X GRAPH.
        Always end the code with plt.show()
        Your code:
        """)
        code_to_analyse = code_for_analysis_check.text.strip()

        print("\n3) Checking code according to requirement")
        code_to_analyse_cleaned = re.sub(r"^```python\n|```$", "", code_to_analyse, flags=re.MULTILINE).strip()

        print('-' * 10)
        print(code_to_analyse_cleaned)
        print('-' * 10)

        ######################

        print("\n4) Executing NetworkX code")
        global_vars = {"G_adb": G_adb, "nx": nx, "plt": plt}
        local_vars = {}

        try:
            exec(code_to_analyse_cleaned, global_vars, local_vars)
        except Exception as e:
            print(f"EXEC ERROR: {e}")
            return f"EXEC ERROR: {e}"

        print('-' * 10)
        FINAL_RESULT = local_vars.get("FINAL_RESULT", "No result generated.")
        print(f"FINAL_RESULT: {FINAL_RESULT}")
        print('-' * 10)

    ######################

    # Displaying the plot directly (no need for IPython's Image class)
        
        print("3) Formulating final answer")

        nx_to_text_response = self.model.generate_content(f"""
            I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

            I have the following graph analysis query: {query}.

            I have executed the following Python code to help me answer my query:

            ---
            {code_to_analyse_cleaned}
            ---

            The `FINAL_RESULT` variable is set to the following: {FINAL_RESULT}.

            Based on my original Query and `FINAL_RESULT`, generate a short and concise response.
            to answer my query.

            Answer the question in simple terms by explaning the output in BUSINESS TERMS ONLY.
            Make sure to help the user understand the plot.
            The answer should say how the plot is solving the given query. Explain in 30 words.

            Your response:
        """)
        print("Description")
        print(nx_to_text_response.text.strip())
        return nx_to_text_response.text.strip()










# Define tools with descriptions

    def analyse_graph_n_visualize(self,query):
        tools = [
        {
            "tool_name": "analyse_networkx",
            "tool_description": (
                "This tool applies a NetworkX algorithm to the ArangoDB graph to analyze "
                "the structure and relationships between departments. It is useful for queries "
                "about collaboration, influence, and data-driven decision-making."
            ),
        },
        {
            "tool_name": "visualize_graph",
            "tool_description": (
                "This tool generates a NetworkX-based visualization of the graph based on the query. "
                "It is used for queries that require a heatmap, centrality diagrams, or network structure visualization."
            ),
        },
    ]

        """
        Determines the most appropriate tool (analyse_networkx or visualize_graph) based on the given query.
        
        Args:
            query (str): A natural language query related to graph analysis.

        Returns:
            str: The output from the selected tool.
        """

    

        # AI-powered tool selection prompt
        system_prompt = (
            "You have access to the following tools:\n"
            f"{tools}\n"
            f"Query: {query}\n\n"
            "Decide which tool is best suited for answering the query:\n"
            "- Use 'analyse_networkx' for analytical queries like centrality, collaboration, or decision-making.\n"
            "- Use 'visualize_graph' for visualization queries like heatmaps or network diagrams.\n\n"
            "ONLY return the tool name as a single word: 'analyse_networkx' or 'visualize_graph'."
        )

        # Get the tool name from the AI model
        tool_name = self.model.generate_content(system_prompt).text.strip()
        print(f"Selected tool: {tool_name}")

        # Execute the chosen tool
        if tool_name == "analyse_networkx":
            return self.analyse_networkx(query)
        elif tool_name == "visualize_graph":
            return self.visualize_graph(query)
        else:
            return "No appropriate tool available for this query."


    def answer_query_benefactor(self,query):

        try:
            answer_to_general_query = self.model.generate_content(f"""
            I have a NetworkX Graph called `G_adb`. It has the following schema: {self.arango_schema}

            Assume the graph is about a large institution named University of Oxford. 
            You are free to assume data for University of Oxford beyond the graph daa points.
            You are a research analyser who is helping benefactors ( people who fund the research) with research opportunities from that institution.
            Your task is to answer the given query for benefactors based on research opportunities in Europe.
            Provide relevant answers based on the research conditions in Europe only.
            Provide unbiasted correct response. Be polite and friendly in your answer. Give responses within 100 words only.
            Query: {query}
            Your answer is:


            """)

            answer_to_general_query = answer_to_general_query.text.strip()
            return answer_to_general_query
        except Exception as e:
            print(f"An error occured {e}")
