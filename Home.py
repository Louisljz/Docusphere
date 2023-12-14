import streamlit as st
import pinecone
import langchain
import os
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from streamlit_extras.switch_page_button import switch_page


langchain.debug = True

st.set_page_config('Home', '📖')
st.title('Docusphere')
st.write('Connect your Pinecone VectorDB with OpenAI Embedding Option.')


api_key = st.text_input('API Key:', placeholder="Pinecone API Key")
if not api_key:
    st.warning('Please use your API Key')
env = st.text_input('Environment:', placeholder="Pinecone Environment")
if not env:
    st.warning('Please use your Environment')
index_name = st.text_input('Index Name:', placeholder="Pinecone Index Name")
if not index_name:
    st.warning('Please use your Index Name')


if st.button('connect', use_container_width=True):
    pinecone.init(api_key=api_key, environment=env)
    st.session_state.vector_store = Pinecone.from_existing_index(index_name, OpenAIEmbeddings())
    st.success('Pinecone DB connected!')
    switch_page('Ingest Documents')
