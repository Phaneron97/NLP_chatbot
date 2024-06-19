import numpy as np

class VectorDB:
    def __init__(self):
        self.data = []

    def add_item(self, text, vector):
        self.data.append((text, vector))

    def search(self, query_vector, top_n=5):
        similarities = [(text, np.dot(vector, query_vector)) for text, vector in self.data]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
