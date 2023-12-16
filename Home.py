import streamlit as st
from streamlit_extras.switch_page_button import switch_page

import os
import pinecone

import langchain
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings

langchain.debug = True

st.set_page_config('Home', '📖')
st.title('Docusphere')
st.write('Connect your Pinecone VectorDB with OpenAI Embedding Option.')

option = st.selectbox('Select a model:', [' ','OpenAI', 'Huggingface'], index=0 ,placeholder='Select a model')

if option == 'OpenAI':
    api_key = st.text_input('API Key:', type='password')
    env = st.text_input('Environment:')
    index_name = st.text_input('Index Name:')

    if api_key and env and index_name and st.button('connect', use_container_width=True): 
        pinecone.init(api_key=api_key, environment=env)
        st.session_state.vector_store = Pinecone.from_existing_index(index_name, OpenAIEmbeddings())
        st.success('Pinecone DB connected!')
        switch_page('Ingest Documents')


elif option == 'Huggingface':
    st.info('Coming soon!')

else:
    st.info('Select a model to continue 👆')