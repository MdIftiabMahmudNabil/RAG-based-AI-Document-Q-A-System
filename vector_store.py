import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

class VectorStore:
    """Store and search document chunks with embeddings"""
    
    def __init__(self):
        self.chunks = []
        self.embeddings = []
        self.metadata = []
    
    def add_documents(self, chunks: List[str], embeddings: List[List[float]], document_name: str):
        """Add document chunks and embeddings to the store"""
        for chunk, embedding in zip(chunks, embeddings):
            self.chunks.append(chunk)
            self.embeddings.append(embedding)
            self.metadata.append({"document": document_name})
    
    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, float, dict]]:
        """Search for most similar chunks"""
        if not self.embeddings:
            return []
        
        # Convert to numpy arrays
        query_emb = np.array(query_embedding).reshape(1, -1)
        doc_embs = np.array(self.embeddings)
        
        # Calculate cosine similarities
        similarities = cosine_similarity(query_emb, doc_embs)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return chunks with similarities and metadata
        results = []
        for idx in top_indices:
            results.append((
                self.chunks[idx],
                float(similarities[idx]),
                self.metadata[idx]
            ))
        
        return results
    
    def clear(self):
        """Clear all stored documents"""
        self.chunks = []
        self.embeddings = []
        self.metadata = []
