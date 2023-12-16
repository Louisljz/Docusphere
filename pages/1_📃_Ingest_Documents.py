import streamlit as st
from openai import OpenAI
import os
from langchain.document_loaders import (
    WebBaseLoader, PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader, 
    UnstructuredPowerPointLoader, UnstructuredExcelLoader
)
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


st.set_page_config('Ingest Documents', '📃')
st.title('Ingest Documents 📃')

def upload_docs(documents):
    doc_splits = text_splitter.split_documents(documents)
    st.session_state.vector_store.add_documents(doc_splits)

if 'vector_store' in st.session_state:
    client = OpenAI()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024, chunk_overlap=100
    )

    media = st.selectbox('Choose media type:', ['Documents', 'Audio', 'Webpages'])

    if media == 'Webpages':
        web_url = st.text_input('Link to webpage:')
        if web_url:
            loader = WebBaseLoader(web_url)
            documents = loader.load()
            
            upload_docs(documents)
            st.info('Web page scraped!')


    elif media == 'Documents':
        doc_files = st.file_uploader('Upload documents:', accept_multiple_files=True,
                type=['txt', 'pdf', 'doc', 'docx', 'ppt',  'pptx', 'xls', 'xlsx'])
        if doc_files:
            documents = []
            for file in doc_files:
                filepath = os.path.join('temp', file.name)
                with open(filepath, 'wb') as f:
                    f.write(file.read())
                
                if file.name.endswith(".pdf"):
                    loader = PyPDFLoader(filepath)
                elif file.name.endswith('.txt'):
                    loader = TextLoader(filepath)
                elif file.name.endswith('.doc') or file.name.endswith('.docx'):
                    loader = UnstructuredWordDocumentLoader(filepath)
                elif file.name.endswith('.ppt') or file.name.endswith('.pptx'):
                    loader = UnstructuredPowerPointLoader(filepath)
                elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                    loader = UnstructuredExcelLoader(filepath)
                
                documents.extend(loader.load())
                os.remove(filepath)
            
            upload_docs(documents)
            st.info('Document content extracted!')

    else:
        audio_file = st.file_uploader('Upload video/audio:', type=['mp3', 'mp4', 'm4a'])
        if audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

            with st.expander('transcript'):
                st.write(transcript.text)

            document = Document(page_content=transcript.text, metadata={'source': audio_file.name})
            
            upload_docs([document])
            st.info('Video/Audio Transcribed!')

else:

    st.warning('Connect your Pinecone DB first!')
