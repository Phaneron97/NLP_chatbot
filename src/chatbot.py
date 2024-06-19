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
        print(preprocessed_query)
        query_vector = self.embedding.embed_text([preprocessed_query])[0]
        print(query_vector)
        results = self.vectordb.search(query_vector)
        print(results)
        response, source = self.format_response(results)
        print(response)
        print(source)
        return response, source

    def format_response(self, results):
        # Ensure results contain tuples with the correct structure
        response_text = " ".join([text for text, _, _ in results])
        source = results[0][2] if results else "No source found"
        return response_text, source
