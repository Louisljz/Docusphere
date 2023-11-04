import streamlit as st
import os

from langchain.document_loaders import (
    AsyncHtmlLoader, PyPDFLoader, Docx2txtLoader, TextLoader
)
from langchain.document_transformers import Html2TextTransformer

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter


st.set_page_config('Ingest Documents', '📃')
st.title('Ingest Documents 📃')

def clear_temp(folder_path='temp'):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=80
)

media = st.selectbox('Choose media type:', ['Websites', 'Documents', 'YT Videos'])

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
    files = st.file_uploader('Upload documents:', 
                ['pdf', 'doc', 'docx', 'txt'], accept_multiple_files=True)
    if files:
        documents = []
        for file in files:

            filepath = os.path.join('temp', file.name)
            with open(filepath, 'wb') as f:
                f.write(file.read())
            
            if file.name.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            elif file.name.endswith('.docx') or file.name.endswith('.doc'):
                loader = Docx2txtLoader(filepath)
            elif file.name.endswith('.txt'):
                loader = TextLoader(filepath)
            
            documents.extend(loader.load())

        docs = text_splitter.split_documents(documents)
        st.session_state.documents.extend(docs)
        clear_temp()
        st.info('Document content extracted!')

else:
    yt_url = st.text_input('Youtube Video URL:')
    if yt_url:
        loader = GenericLoader(YoutubeAudioLoader([yt_url], 'temp'), OpenAIWhisperParser())
        transcript = loader.load()
        docs = text_splitter.split_documents(transcript)
        st.session_state.documents.extend(docs)
        clear_temp()
        st.info('YT audio transcripted!')
