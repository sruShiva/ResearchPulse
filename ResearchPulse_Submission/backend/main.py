from utilities.arango_fetcher import ArangoDBFetcher
from personas.student import StudentPersona
from  personas.professor import ProfessorPersona
from personas.benefactor import BenefactorPersona
import os
import dotenv 
import networkx as nx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
# Load environment variables from a .env file
dotenv.load_dotenv()

# Example: Access an environment variable

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
# self, graph_name, edge_definitions, G_adb, schema,nx
student_persona = StudentPersona(graph_name, G_adb, graph_schema,nx)
professor_persona = ProfessorPersona(graph_name, G_adb, graph_schema,nx)
benefactor_persona = BenefactorPersona(graph_name, G_adb, graph_schema,nx)
app = FastAPI()

# Enable CORS (Allow frontend apps to access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],# Change to specific domains for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def home():
    return {"message": "Welcome to Research Pulse!"}

@app.get("/api/answer-student-queries")
def answer_student_queries(intention:str, query:str):

    try:
        if intention == "graph":
            ans= student_persona.query_graph(query)
        else:
            ans = student_persona.answer_query_graph(query)

        return ans
    except Exception as e:
        print(f"An error occured {e}")
        return "oops! Something went wrong, please try again!"
    

@app.get("/api/answer-professor-queries")
def answer_professor_queries(intention:str, query:str):

    try:
        if intention == "graph":
            ans= professor_persona.query_graph(query)
        else:
            ans = professor_persona.answer_query_professor(query)

        return ans
    except Exception as e:
        print(f"An error occured {e}")
        return "oops! Something went wrong, please try again!"
    
    
@app.get("/api/answer-benefactor-queries")
def answer_benefactor_queries(intention:str, query:str):

    try:
        if intention == "graph":
            ans= benefactor_persona.analyse_networkx(query)
           
        else:
            ans = benefactor_persona.answer_query_benefactor(query)

        return ans
    except Exception as e:
        print(f"An error occured {e}")
        return "oops! Something went wrong, please try again!"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)