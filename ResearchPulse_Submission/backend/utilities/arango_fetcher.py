from arango import ArangoClient
import networkx as nx
import os
from langchain_community.graphs import ArangoGraph
import os
import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

# Example: Access an environment variable


class ArangoDBFetcher:
    def __init__(self, db_name, username, password, host_url):
        """Initialize the ArangoDB connection."""
        self.client = ArangoClient(hosts=host_url, verify_override= False)
        self.db = self.client.db(db_name, username=username, password=password)
        self.arango_graph = ArangoGraph(self.db)
        self.edge_collections = [col['name'] for col in self.db.collections() if col['type'] == 'edge']
        
    def get_arango_db(self):
        return  self.db 
    
    def query(self, aql_query):
        """Executes an AQL query on the database and returns the result."""
        try:
            cursor = self.db.aql.execute(aql_query)
            return list(cursor)  # Convert cursor to list for easy handling
        except Exception as e:
            return f"Error executing AQL: {e}"

    def get_graph_schema(self):
        """Fetches schema details of the graph (edges, vertices)."""
        try:
            
            return self.arango_graph
        except Exception as e:
            return f"Error fetching graph schema: {e}"
    
    def get_edge_definitions(self):
        """Retrieves edge definitions of the given graph."""
        try:
            return self.arango_graph.schema['Graph Schema'][0]['edge_definitions']
        except Exception as e:
            return f"Error fetching edge definitions: {e}"
        
    def get_graph_name(self):
        """Retrieves edge definitions of the given graph."""
        try:
            return self.arango_graph.schema['Graph Schema'][0]['graph_name']
        except Exception as e:
            return f"Error fetching edge definitions: {e}"
        

    def fetch_graph_data(self):
        """Fetches edges from ArangoDB and converts them into a NetworkX graph."""
        query = f"FOR edge IN {self.edge_collections[0]} RETURN edge"
        cursor = self.query( query)
        print("Curosor--------------------->")
      
        G = nx.Graph()  # Use nx.DiGraph() for directed graphs

        for edge in cursor:
            print
            from_node = edge["_from"].split("/")[-1]  # Extract actual node ID
            to_node = edge["_to"].split("/")[-1]
            G.add_edge(from_node, to_node)

        return G
