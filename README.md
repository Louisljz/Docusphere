
# Document-Based Question-Answering System

## Table of Contents
- [Document Loader](#document-loader)
- [Text Splitters](#text-splitters)
- [Embeddings](#embeddings)
- [Vector Store](#vector-store)
- [LLM (Large Language Model)](#llm)
- [RetrievalQAChainType](#retrievalqachaaintype)
- [API Testing](#api-testing)
- [Installation and Setup](#installation-and-setup)

---

## Document Loader

**Choice**: PDF Loader  
**Documentation**: [Document Loaders](https://python.langchain.com/docs/integrations/document_loaders/)  
**Extra**: Speech transcription from audio/video [AssemblyAI](https://www.assemblyai.com/blog/retrieval-augmented-generation-audio-langchain/)

---

## Text Splitters

**Choice**: RecursiveCharacterTextSplitter  
**Documentation**: [Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/#text-splitters)

---

## Embeddings

**Choice**: [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)  
**Documentation**: [Text Embedding](https://python.langchain.com/docs/integrations/text_embedding/)

---

## Vector Store

**Choice**: FAISS  
**Documentation**: [Vector Store](https://python.langchain.com/docs/integrations/vectorstores/)  
**Info**: Local like ChromaDB or FAISS / Cloud like Pinecone or Weaviate

---

## LLM (Large Language Model)

**Choice**: [flan-t5-large](https://huggingface.co/google/flan-t5-large)  
**Documentation**: [LLMs](https://python.langchain.com/docs/integrations/llms/)

---

## RetrievalQAChainType

**Choice**: map_reduce  
**Documentation**: Not provided

---

## API Testing

**Choice**: FastAPI  
**Documentation**: Not provided

## Installation and Setup

### Installing Requirements

You can install the necessary Python packages using pip. 
Run this command in a virtual environment:

```bash
pip install -r requirements.txt
```

### Cloning Hugging Face Model

To clone the Hugging Face embeddings repository, run the following command:

```bash
git lfs install 
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 
```

### Configure HUGGINGFACEHUB_API_TOKEN

Create a `.env` file and paste your READ access token from [here](https://huggingface.co/settings/tokens)

### Starting FastAPI Server

To start the FastAPI server using Uvicorn, navigate to the directory where your FastAPI application is located and run:

```bash
uvicorn app:app --reload
```

## References

- https://www.linkedin.com/pulse/get-insight-from-your-business-data-build-llm-application-jain/