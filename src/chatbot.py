import numpy as np
from embedding import Embedding  # Importing the Embedding class
from vectordb import VectorDB  # Importing the VectorDB class

class Chatbot:
    def __init__(self):
        """
        Initializes the Chatbot with an embedding model and a vector database.
        """
        self.embedding = Embedding()  # Instance of the embedding model
        self.vectordb = VectorDB()  # Instance of the vector database

    def generate_response(self, user_input):
        """
        Generates a response to the user input by searching the vector database.
        """
        # Embed the user input text to obtain a query vector
        query_vector = self.embedding.embed_text([user_input])[0]
        
        # Search for the most similar item in the vector database
        search_result = self.vectordb.search(query_vector)
        print(search_result)
        
        if search_result is not None:
            # If a match is found, unpack the search result
            best_match, source_section, source_file = search_result
            
            # Limit the response to a max of 1000 characters and cut off at the end of a sentence
            response = self.truncate_response(best_match, max_length=1000)
            # Create a source reference
            source = f"{source_section}, from file: {source_file}"
        else:
            # If no match is found, return a default response
            response = "I'm sorry, I couldn't find any relevant information."
            source = "No source available."
        
        return response, source

    def truncate_response(self, text, max_length):
        """
        Truncates the response text to a maximum length, cutting off at the end of a sentence.
        """
        if len(text) <= max_length:
            return text
        
        truncated_text = text[:max_length]
        # Find the last period within the truncated text
        last_period_index = truncated_text.rfind('.')
        
        if last_period_index != -1:
            # Cut off at the last period
            return truncated_text[:last_period_index + 1]
        else:
            # If no period is found, return the truncated text as is
            return truncated_text + '...'
