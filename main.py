import os
import glob
from pathlib import Path
from document_processor import DocumentProcessor
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from qa_system import QASystem

class RAGSystem:
    """Main RAG Document Q&A System"""
    
    def __init__(self):
        self.processor = DocumentProcessor()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.qa_system = QASystem()
        print("✓ RAG System initialized")
    
    def add_document(self, file_path: str):
        """Add a document to the system"""
        print(f"\n📄 Processing: {file_path}")
        
        # Extract and chunk text
        chunks = self.processor.process_document(file_path)
        print(f"✓ Created {len(chunks)} chunks")
        
        # Generate embeddings
        print("🔄 Generating embeddings...")
        embeddings = self.embedding_gen.generate_embeddings_batch(chunks)
        print("✓ Embeddings generated")
        
        # Add to vector store
        document_name = os.path.basename(file_path)
        self.vector_store.add_documents(chunks, embeddings, document_name)
        print(f"✓ Document added to vector store")
    
    def ask_question(self, question: str) -> str:
        """Ask a question and get an answer"""
        print(f"\n❓ Question: {question}")
        
        # Generate query embedding
        query_embedding = self.embedding_gen.generate_embedding(question)
        
        # Search for relevant chunks
        results = self.vector_store.search(query_embedding, top_k=3)
        
        if not results:
            return "No documents have been added yet."
        
        print(f"✓ Found {len(results)} relevant chunks")
        
        # Generate answer
        print("🤖 Generating answer...")
        answer = self.qa_system.generate_answer(question, results)
        
        return answer

def find_documents_in_directory(directory: str) -> list:
    """Find all PDF and DOCX files in a directory"""
    files = []
    extensions = ['*.pdf', '*.docx', '*.txt']
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, ext)))
        files.extend(glob.glob(os.path.join(directory, '**', ext), recursive=True))
    return sorted(set(files))

def select_file_interactively() -> str:
    """Interactive file selection"""
    print("\n📁 File Selection Options:")
    print("1. Enter full file path")
    print("2. Browse Downloads folder")
    print("3. Browse Documents folder")
    print("4. Browse current directory")
    print("5. Search in a specific folder")
    
    choice = input("\nChoose option (1-5): ").strip()
    
    if choice == "1":
        return input("Enter full file path: ").strip()
    
    elif choice == "2":
        downloads = str(Path.home() / "Downloads")
        return browse_directory(downloads)
    
    elif choice == "3":
        documents = str(Path.home() / "Documents")
        return browse_directory(documents)
    
    elif choice == "4":
        current = os.getcwd()
        return browse_directory(current)
    
    elif choice == "5":
        folder = input("Enter folder path: ").strip()
        if os.path.exists(folder):
            return browse_directory(folder)
        else:
            print("❌ Folder not found!")
            return ""
    
    else:
        print("❌ Invalid option!")
        return ""

def browse_directory(directory: str) -> str:
    """Browse and select a file from directory"""
    print(f"\n📂 Searching in: {directory}")
    files = find_documents_in_directory(directory)
    
    if not files:
        print("❌ No PDF, DOCX, or TXT files found in this directory!")
        return ""
    
    print(f"\n✓ Found {len(files)} documents:")
    print("-" * 60)
    for i, file in enumerate(files, 1):
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file) / 1024  # KB
        print(f"{i}. {file_name} ({file_size:.1f} KB)")
    print("-" * 60)
    
    try:
        selection = int(input(f"\nSelect file number (1-{len(files)}): ").strip())
        if 1 <= selection <= len(files):
            return files[selection - 1]
        else:
            print("❌ Invalid selection!")
            return ""
    except ValueError:
        print("❌ Please enter a valid number!")
        return ""

def main():
    """Main function to run the RAG system"""
    print("=" * 60)
    print("🚀 AI Document Q&A System (RAG-based)")
    print("=" * 60)
    
    # Initialize system
    rag = RAGSystem()
    
    # Interactive loop
    while True:
        print("\n" + "=" * 60)
        print("Options:")
        print("1. Add document")
        print("2. Ask question")
        print("3. Clear documents")
        print("4. Exit")
        print("=" * 60)
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            file_path = select_file_interactively()
            if file_path and os.path.exists(file_path):
                try:
                    rag.add_document(file_path)
                    print("✓ Document successfully added!")
                except Exception as e:
                    print(f"❌ Error: {e}")
            elif file_path:
                print("❌ File not found!")
        
        elif choice == "2":
            question = input("Enter your question: ").strip()
            if question:
                try:
                    answer = rag.ask_question(question)
                    print("\n" + "=" * 60)
                    print("💡 Answer:")
                    print("-" * 60)
                    print(answer)
                    print("=" * 60)
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                print("❌ Please enter a question!")
        
        elif choice == "3":
            rag.vector_store.clear()
            print("✓ All documents cleared!")
        
        elif choice == "4":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
