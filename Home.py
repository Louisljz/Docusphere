import streamlit as st
import pinecone


if "vector_store" not in st.session_state:
    st.session_state.vector_store = {'type': 'faiss', 'name': ''}

st.set_page_config('Home', '📖')
st.title('Docusphere HomePage 📖')

db = st.selectbox('Choose database to use:', ['in memory (FAISS)', 'cloud (pinecone)'])

if db == 'cloud (pinecone)':
    api_key = st.text_input('Pinecone API Key:')
    env = st.text_input('Pinecone Environment:')
    index_name = st.text_input('Pinecone Index Name:')

    if api_key and env and index_name:
        pinecone.init(api_key=api_key, environment=env)
        st.success('Pinecone DB connected!')
        st.session_state.vector_store = {'type': 'pinecone', 'name': index_name}

else:
    st.session_state.vector_store = {'type': 'faiss', 'name': ''}
