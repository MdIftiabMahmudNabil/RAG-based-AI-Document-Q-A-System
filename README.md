# AI Document Q&A System (RAG-based)

Upload documents (PDF, DOCX) and ask questions — the system retrieves context using embeddings and generates AI-based answers.

## Features

- 📄 **Document Processing**: Extract text from PDF and DOCX files
- 🔍 **Smart Chunking**: Split documents into manageable chunks with overlap
- 🤖 **AI-Powered Embeddings**: Generate embeddings using GitHub Models API
- 🎯 **Semantic Search**: Find relevant chunks using cosine similarity
- 💬 **Q&A Generation**: Answer questions based on document context
- 🖥️ **Interactive CLI**: Easy-to-use command-line interface

## Prerequisites

- Python 3.8 or higher
- GitHub account with access to GitHub Models
- GitHub Personal Access Token with "models" scope

## Setup Instructions

### 1. Get Your GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "RAG System")
4. Select the **"models"** scope
5. Click "Generate token"
6. **Copy the token** (you won't be able to see it again!)

### 2. Configure Environment

Edit the `.env` file and replace `your_github_token_here` with your actual token:

```
GITHUB_TOKEN=github_pat_YOUR_ACTUAL_TOKEN_HERE
```

### 3. Create Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Or if using Command Prompt
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- `openai` - For GitHub Models API
- `python-dotenv` - For environment variable management
- `PyPDF2` - For PDF text extraction
- `python-docx` - For DOCX text extraction
- `numpy` - For numerical operations
- `scikit-learn` - For cosine similarity calculations

## Usage

### Running the Application

```powershell
python main.py
```

### Interactive Menu

The application provides four options:

1. **Add document** - Upload a PDF or DOCX file to the system
2. **Ask question** - Query the documents you've added
3. **Clear documents** - Remove all documents from memory
4. **Exit** - Close the application

### Example Workflow

```
🚀 RAG Document Q&A System
============================================================
✓ RAG System initialized

============================================================
Options:
1. Add document
2. Ask question
3. Clear documents
4. Exit
============================================================

Enter choice (1-4): 1
Enter document path (PDF or DOCX): research_paper.pdf

📄 Processing: research_paper.pdf
✓ Created 45 chunks
🔄 Generating embeddings...
✓ Embeddings generated
✓ Document added to vector store
✓ Document successfully added!

Enter choice (1-4): 2
Enter your question: What is the main conclusion?

❓ Question: What is the main conclusion?
✓ Found 3 relevant chunks
🤖 Generating answer...

============================================================
💡 Answer:
------------------------------------------------------------
The main conclusion of the research paper is that...
============================================================
```

## Project Structure

```
rag-document-qa/
├── .env                    # Environment variables (GitHub token)
├── requirements.txt        # Python dependencies
├── document_processor.py   # Document extraction and chunking
├── embeddings.py          # Embedding generation with GitHub Models
├── vector_store.py        # Vector storage and similarity search
├── qa_system.py           # Question answering logic
├── main.py                # Main application and CLI
└── README.md              # This file
```

## How It Works

### 1. Document Processing
- Extracts text from PDF/DOCX files
- Splits text into 500-word chunks with 50-word overlap
- Preserves context across chunk boundaries

### 2. Embedding Generation
- Uses `text-embedding-3-small` model from GitHub Models
- Converts text chunks into vector representations
- Enables semantic similarity search

### 3. Vector Storage
- Stores chunks with their embeddings
- Performs cosine similarity search
- Returns top 3 most relevant chunks

### 4. Answer Generation
- Uses `gpt-4o-mini` model from GitHub Models
- Provides context from relevant chunks
- Generates coherent answers based on document content

## Troubleshooting

### Authentication Error
```
❌ Error: Incorrect API key provided
```
**Solution**: Check that your GitHub token is correct in `.env` file and has "models" scope.

### Import Errors
```
❌ ModuleNotFoundError: No module named 'openai'
```
**Solution**: Make sure virtual environment is activated and run `pip install -r requirements.txt`

### PDF Extraction Issues
```
❌ Error: Failed to extract text from PDF
```
**Solution**: Some PDFs are image-based or encrypted. Try converting to text-based PDF or use OCR tools.

### Memory Issues
```
❌ MemoryError
```
**Solution**: For large documents, reduce `chunk_size` in `document_processor.py` or process fewer documents at once.

## Advanced Usage

### Custom Chunk Size

Edit `document_processor.py` line 25 to change chunk size:

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
```

### Different Models

Edit `embeddings.py` or `qa_system.py` to use different models:

```python
self.model = "text-embedding-3-large"  # For better embeddings
self.model = "gpt-4o"                  # For better answers
```

### Batch Processing

To process multiple documents at startup, modify `main.py`:

```python
def main():
    rag = RAGSystem()
    
    # Auto-load documents
    documents = ["doc1.pdf", "doc2.pdf", "doc3.docx"]
    for doc in documents:
        if os.path.exists(doc):
            rag.add_document(doc)
    
    # Continue with interactive loop...
```

## Future Enhancements

- [ ] Add support for TXT and HTML files
- [ ] Implement caching for embeddings
- [ ] Add web interface with Gradio
- [ ] Support for multiple languages
- [ ] Document metadata tracking (page numbers, sections)
- [ ] Export Q&A history
- [ ] Async processing for faster embedding generation
- [ ] Add progress bars with `tqdm`

## Resources

- [GitHub Models Documentation](https://github.com/marketplace/models)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [RAG Research Paper](https://arxiv.org/abs/2005.11401)
- [Vector Search Concepts](https://www.pinecone.io/learn/vector-search/)

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to submit issues and enhancement requests!

---

**Built with GitHub Models API** 🚀
