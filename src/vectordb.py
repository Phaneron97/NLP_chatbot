import numpy as np

class VectorDB:
    def __init__(self):
        """
        Initializes an empty vector database.
        """
        self.data = {}

    def add_item(self, item, vector):
        """
        Adds an item and its corresponding vector to the database.
        """
        self.data[item] = vector

    def search(self, query_vector):
        """
        Searches for the most similar item in the database to the query vector.
        """
        best_match = None
        best_similarity = -np.inf  # Initialize best similarity with negative infinity

        for item, item_vector in self.data.items():
            # Calculate cosine similarity between the query vector and the item vector
            similarity = np.dot(query_vector, item_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(item_vector))
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = item
        
        print(f"Best match: {best_match}, Similarity: {best_similarity}")
        return best_match
