import numpy as np

class VectorDB:
    def __init__(self):
        self.data = {}

    def add_item(self, item, vector):
        self.data[item] = vector

    def search(self, query_vector):
        best_match = None
        best_similarity = -np.inf

        for item, item_vector in self.data.items():
            similarity = np.dot(query_vector, item_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(item_vector))
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = item
        print(f"Best match: {best_match}, Similarity: {best_similarity}")
        return best_match
