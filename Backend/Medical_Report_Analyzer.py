import os
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import warnings
import tempfile
import shutil
from pathlib import Path
warnings.filterwarnings('ignore')

load_dotenv()
gemini_api_key = os.environ.get("GEMINI_API_KEY")

def save_temp_file(file_data, file_type: str = 'pdf') -> str:
    temp_dir = Path("temp_files")
    temp_dir.mkdir(exist_ok=True)
    
    if file_type != 'pdf':
        raise ValueError("Only PDF files are supported.")
    
    extension = '.pdf'
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=extension, dir=temp_dir)
    temp_path = temp_file.name

    try:
        if isinstance(file_data, (str, Path)):
            with open(file_data, 'rb') as src, open(temp_path, 'wb') as dst:
                shutil.copyfileobj(src, dst)
        else:  # file-like object
            with open(temp_path, 'wb') as dst:
                shutil.copyfileobj(file_data, dst)
    except Exception as e:
        cleanup_temp_file(temp_path)
        raise Exception(f"Error saving file: {str(e)}")

    return temp_path

def cleanup_temp_file(temp_path: str):
    try:
        os.remove(temp_path)
    except Exception as e:
        print(f"Error cleaning up temporary file: {e}")

def rag_pipeline(file_data, file_type: str = 'pdf'):
    if file_type != 'pdf':
        raise ValueError("Only PDF files are supported.")
    try:
        temp_file_path = save_temp_file(file_data, file_type)
        
        # Load and split PDF
        loader = PyMuPDFLoader(temp_file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=gemini_api_key
        )
        
        vector_store = FAISS.from_documents(chunks, embeddings)
        model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  
            google_api_key=gemini_api_key,
            temperature=0.7
        )
        
        cleanup_temp_file(temp_file_path)
        return vector_store, model

    except Exception as e:
        if 'temp_file_path' in locals():
            cleanup_temp_file(temp_file_path)
        raise e

def query_medical_report(vector_store, model, query: str):
    docs = vector_store.similarity_search(query)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"""Based on the following medical report context, please answer the question.
If you cannot find the answer in the context, say so.
Context: {context}
Question: {query}
Answer:"""
    response = model.invoke(prompt)
    return response.content

if __name__ == "__main__":
    pdf_path = r"C:\Users\HP\Desktop\Health_Care_Assitant\Healthcare-Multi-Specialist-AI-Assistant\Backend\CBC_report.pdf"
    vector_store, model = rag_pipeline(pdf_path, 'pdf')
    query = "what about rbc?"
    response = query_medical_report(vector_store=vector_store, model=model, query=query)
    print("Medical Report Analysis:")
    print(response)
