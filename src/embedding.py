from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        print(f"Loaded model: {model_name}")  # Debug: Confirm model load

    def embed_text(self, texts):
        embeddings = self.model.encode(texts)
        print("Generated embeddings:", embeddings)  # Debug: Print embeddings
        return embeddings
