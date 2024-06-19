import ollama
from vectordb import VectorDB
from embedding import Embedding

class Chatbot:
    def __init__(self):
        self.embedding = Embedding()
        self.vectordb = VectorDB()
        self.max_length = 1000  # Set a maximum length for the response

    def preprocess_query(self, query):
        return query.lower()

    def generate_response(self, query):
        preprocessed_query = self.preprocess_query(query)
        query_vector = self.embedding.embed_text([preprocessed_query])[0]
        results = self.vectordb.search(query_vector)
        response, source = self.format_response(results)
        return response, source

    def format_response(self, results):
        if not results:
            return "I'm sorry, I couldn't find the information you're looking for.", ""
        
        response = results[0][0]  # Get the most relevant section
        source = results[0][1]  # Get the source information
        if len(response) > self.max_length:
            response = self.trim_response(response, self.max_length)
        
        return response, source

    def trim_response(self, response, max_length):
        if len(response) <= max_length:
            return response
        
        trimmed_response = response[:max_length]
        last_period_index = trimmed_response.rfind('. ')
        if last_period_index != -1:
            return trimmed_response[:last_period_index + 1]
        
        return trimmed_response  # Fallback to returning the trimmed response as is
