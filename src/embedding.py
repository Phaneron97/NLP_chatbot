from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initializes the Embedding model using SentenceTransformer.
        """
        self.model = SentenceTransformer(model_name)  # Load the specified SentenceTransformer model

    def embed_text(self, texts):
        """
        Generates embeddings for a list of texts.
        """
        return self.model.encode(texts)  # Generate and return embeddings for the input texts
