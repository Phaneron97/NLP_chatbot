import ollama
from vectordb import VectorDB
from embedding import Embedding

class Chatbot:
    def __init__(self):
        self.embedding = Embedding()
        self.vectordb = VectorDB()

    def preprocess_query(self, query):
        return query.lower()    

    def generate_response(self, query):
        preprocessed_query = self.preprocess_query(query)
        print(f"Preprocessed Query: {preprocessed_query}")  # Debug: Print preprocessed query
        query_vector = self.embedding.embed_text([preprocessed_query])[0]
        print(f"Query Vector: {query_vector[:5]}...")  # Debug: Print a snippet of the query vector
        results = self.vectordb.search(query_vector)
        print(f"Search Results: {results}")  # Debug: Print search results
        response, source = self.format_response(results)
        print(f"Response: {response}")  # Debug: Print response
        print(f"Source: {source}")  # Debug: Print source
        return response, source

    def format_response(self, results):
        # Ensure results contain tuples with the correct structure
        response_text = " ".join([text for text, _, _ in results])
        source = results[0][2] if results else "No source found"
        return response_text, source
