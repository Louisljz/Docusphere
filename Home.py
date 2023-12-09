import streamlit as st
import pinecone
import langchain

from langchain.vectorstores import Pinecone
from langchain.embeddings import HuggingFaceEmbeddings

langchain.debug = True

st.set_page_config('Home', '📖')
st.title('Docusphere HomePage 📖')

@st.cache_data
def load_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

embeddings = load_embeddings()

api_key = st.text_input('Pinecone API Key:')
env = st.text_input('Pinecone Environment:')
index_name = st.text_input('Pinecone Index Name:')

if api_key and env and index_name:
    pinecone.init(api_key=api_key, environment=env)
    index = pinecone.Index(index_name)
    st.session_state.vector_store = Pinecone(index, embeddings, "text")
    st.success('Pinecone DB connected!')
