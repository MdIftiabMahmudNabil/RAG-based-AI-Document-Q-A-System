import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List
import numpy as np

load_dotenv()

class EmbeddingGenerator:
    """Generate embeddings using GitHub Models API"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        self.model = "text-embedding-3-small"
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return response.data[0].embedding
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
