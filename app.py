from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
import shutil
import os

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()

# Embeddings
model_kwargs = {'device':'cpu'}
encode_kwargs = {'normalize_embeddings':False}
embeddings = HuggingFaceEmbeddings(
  model_name = "./all-MiniLM-L6-v2",  
  model_kwargs = model_kwargs,
  encode_kwargs = encode_kwargs
)

# LLM
llm = HuggingFaceHub(
    repo_id='google/flan-t5-large', 
    model_kwargs={"temperature": 0, "max_length": 512}
)

# Prompt Template
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

# API endpoints
app = FastAPI()

@app.post("/ingest/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        # save to tmp file
        file_location = f"tmp/{file.filename}"
        with open(file_location, "wb+") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Document Loaders
        pdfLoader = PyPDFLoader(file_location)
        documents = pdfLoader.load()
        os.remove(file_location)

        # Text Splitters
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = text_splitter.split_documents(documents)

        # Vector Store
        db = FAISS.from_documents(docs, embeddings)
        db.save_local("faiss_index")

        return "PDF content uploaded to DB."
    else:
        return "Invalid file type. Please upload a PDF file."

@app.post("/query/")
async def query(question: str):
    try: 
        vectorstore = FAISS.load_local("faiss_index", embeddings)
        # RAG Chain
        qa_chain = RetrievalQA.from_chain_type(   
            llm=llm,   
            chain_type="stuff",   
            retriever=vectorstore.as_retriever(),   
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} 
        )
        result = qa_chain({"query" : question})
        return result['result']

    except Exception as e:
        print(e)
        return "FAISS DB not yet created. Please ingest at least one document."
