import streamlit as st
import pinecone

from langchain.vectorstores import FAISS, Pinecone
from langchain.embeddings import HuggingFaceEmbeddings


if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

st.set_page_config('Home', '📖')
st.title('Docusphere HomePage 📖')

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = st.selectbox('Choose database to use:', ['in memory (FAISS)', 'cloud (pinecone)'])

if db == 'cloud (pinecone)':
    api_key = st.text_input('Pinecone API Key:')
    env = st.text_input('Pinecone Environment:')
    index_name = st.text_input('Pinecone Index Name:')

    if api_key and env and index_name:
        pinecone.init(api_key=api_key, environment=env)
        index = pinecone.Index(index_name)
        st.session_state.vector_store = Pinecone(index, embeddings.embed_query, "text")
        st.success('Pinecone DB connected!')

else:
    st.session_state.vector_store = FAISS(embeddings.embed_query)
