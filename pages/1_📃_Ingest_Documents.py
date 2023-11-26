import streamlit as st
import os

from langchain.document_loaders import (
    AsyncHtmlLoader, PyPDFLoader, Docx2txtLoader, TextLoader, 
    UnstructuredPowerPointLoader, UnstructuredExcelLoader, 
)
from langchain.document_transformers import Html2TextTransformer
from langchain.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


if "documents" not in st.session_state:
    st.session_state.documents = []

st.set_page_config('Ingest Documents', '📃')
st.title('Ingest Documents 📃')

def clear_temp(folder_path='temp'):
    for file_name in os.listdir(folder_path):
        if not file_name.endswith('.md'):
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=80
)

media = st.selectbox('Choose media type:', ['Documents', 'Video/Audio', 'Websites'])

if media == 'Websites':
    web_url = st.text_input('Link to webpage:')
    if web_url:
        loader = AsyncHtmlLoader(web_url)
        raw_web_content = loader.load()
        html2text = Html2TextTransformer()
        clean_web_content = html2text.transform_documents(raw_web_content)
        docs = text_splitter.split_documents(clean_web_content)
        st.session_state.documents.extend(docs)
        st.info('Web page scraped!')

elif media == 'Documents':
    files = st.file_uploader('Upload documents:', accept_multiple_files=True,
            type=['pdf', 'txt', 'doc', 'docx', 'ppt',  'pptx', 'xls', 'xlsx'])
    if files:
        documents = []
        for file in files:

            filepath = os.path.join('temp', file.name)
            with open(filepath, 'wb') as f:
                f.write(file.read())
            
            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            elif file.name.endswith('.txt'):
                loader = TextLoader(filepath)
            elif file.name.endswith('.doc') or file.name.endswith('.docx'):
                loader = Docx2txtLoader(filepath)
            elif file.name.endswith('.ppt') or file.name.endswith('.pptx'):
                loader = UnstructuredPowerPointLoader(filepath)
            elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
                loader = UnstructuredExcelLoader(filepath)
            
            documents.extend(loader.load())

        docs = text_splitter.split_documents(documents)
        st.session_state.documents.extend(docs)
        clear_temp()
        st.info('Document content extracted!')

else:
    file = st.file_uploader('Upload documents:', type=['mp3', 'mp4'])
    if file:
        filepath = os.path.join('temp', file.name)
        with open(filepath, 'wb') as f:
            f.write(file.read())
        
        loader = AssemblyAIAudioTranscriptLoader(filepath)
        transcript = loader.load()

        docs = text_splitter.split_documents(transcript)
        st.session_state.documents.extend(docs)
        clear_temp()
        st.info('Video/Audio Transcribed!')
