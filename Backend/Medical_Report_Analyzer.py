import os
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import warnings
import tempfile
import shutil
from pathlib import Path
warnings.filterwarnings('ignore')


load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")

def save_temp_pdf(pdf_file) -> str:
    """
    Save uploaded PDF file to a temporary location
    Args:
        pdf_file: The uploaded PDF file
    Returns:
        str: Path to the temporary PDF file
    """
    # Create a temporary directory if it doesn't exist
    temp_dir = Path("temp_pdfs")
    temp_dir.mkdir(exist_ok=True)
    
    # Create a temporary file with .pdf extension
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=temp_dir)
    temp_path = temp_file.name
    
    # Save the uploaded file to the temporary location
    with open(temp_path, 'wb') as f:
        shutil.copyfileobj(pdf_file, f)
    
    return temp_path

def cleanup_temp_pdf(temp_path: str):
    """
    Clean up temporary PDF file after processing
    Args:
        temp_path: Path to the temporary PDF file
    """
    try:
        os.remove(temp_path)
    except Exception as e:
        print(f"Error cleaning up temporary file: {e}")

def rag_pipeline(pdf_file):
    """
    Process PDF through RAG pipeline
    Args:
        pdf_file: The uploaded PDF file
    Returns:
        tuple: (vector_store, llm) for querying
    """
    try:
        # Save PDF to temporary location
        temp_pdf_path = save_temp_pdf(pdf_file)
        
        # Load the PDF document
        loader = PyMuPDFLoader(temp_pdf_path)
        documents = loader.load()
        
        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        
        # Initialize the embedding model
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=gemini_api_key
        )
        
        # Create vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=gemini_api_key,
            temperature=0.7
        )
        
        # Clean up temporary file
        cleanup_temp_pdf(temp_pdf_path)
        
        return vector_store, llm
        
    except Exception as e:
        # Clean up temporary file in case of error
        if 'temp_pdf_path' in locals():
            cleanup_temp_pdf(temp_pdf_path)
        raise e

def query_medical_report(vector_store, llm, query: str):
    # Retrieve relevant documents
    docs = vector_store.similarity_search(query)
    
    # Create context from retrieved documents
    context = "\n".join([doc.page_content for doc in docs])
    
    # Create prompt template
    prompt = f"""Based on the following medical report context, please answer the question.
    If you cannot find the answer in the context, say so.
    
    Context: {context}
    
    Question: {query}
    
    Answer:"""
    
    # Generate response
    response = llm.invoke(prompt)
    return response.content
