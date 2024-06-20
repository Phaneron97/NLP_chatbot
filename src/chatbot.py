import numpy as np
from embedding import Embedding
from vectordb import VectorDB

class Chatbot:
    def __init__(self):
        self.embedding = Embedding()
        self.vectordb = VectorDB()

    def generate_response(self, user_input):
        query_vector = self.embedding.embed_text([user_input])[0]
        search_result = self.vectordb.search(query_vector)
        print(search_result)
        
        if search_result is not None:
            best_match, source_section, source_file = search_result
            response = f"{best_match}"
            source = f"{source_section}, from file: {source_file}"
        else:
            response = "I'm sorry, I couldn't find any relevant information."
            source = "No source available."
        
        return response, source
