import numpy as np

class VectorDB:
    def __init__(self):
        self.data = []

    def add_item(self, item, vector):
        print(f"Adding item: {item}")  # Debug: Print item
        self.data.append((item, vector))

    def search(self, query_vector, top_n=5):
        similarities = [(item, np.dot(vector, query_vector)) for item, vector in self.data]
        similarities.sort(key=lambda x: x[1], reverse=True)
        print(f"Search results: {similarities[:top_n]}")  # Debug: Print search results
        return similarities[:top_n]
