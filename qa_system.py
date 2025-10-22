import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

class QASystem:
    """Generate answers using retrieved context"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("GITHUB_TOKEN"),
        )
        self.model = "gpt-4o-mini"
    
    def generate_answer(self, question: str, context_chunks: List[Tuple[str, float, dict]]) -> str:
        """Generate answer based on retrieved context"""
        
        # Prepare context
        context = "\n\n".join([chunk[0] for chunk in context_chunks])
        
        # Create prompt
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based on the provided context. "
                          "If the answer cannot be found in the context, say so clearly."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer based on the context above:"
            }
        ]
        
        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
