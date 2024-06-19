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
        query_vector = self.embedding.embed_text([preprocessed_query])[0]
        results = self.vectordb.search(query_vector)
        response = self.format_response(results)
        return response

    def format_response(self, results):
        return " ".join([text for text, _ in results])
