from sentence_transformers import SentenceTransformer

class Embedding:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed_text(self, texts):
        return self.model.encode(texts)
