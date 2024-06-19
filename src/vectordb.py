import numpy as np

class VectorDB:
    def __init__(self):
        self.data = {}

    def add_item(self, item, vector):
        self.data[item] = vector

    def search(self, query_vector, top_n=5):
        print(f"Searching with query vector: {query_vector}")
        similarities = []
        for item, vector in self.data:
            sim = np.dot(vector, query_vector)
            similarities.append((item, sim))
            print(f"Item: {item}, Similarity: {sim}, Vector: {vector[:5]}...")  # Debug: Print similarity and snippet of vector
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"Search results: {similarities[:top_n]}")  # Debug: Print sorted search results
        
        return similarities[:top_n]
