import streamlit as st
import openai

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.vectorstores import Pinecone

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationalRetrievalChain


if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config('Retrieve Information', '🔍')
st.title('Retrieve Information 🔍')

@st.cache_resource
def load_models():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    openai.api_key = st.secrets['OPENAI_API_KEY']
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

    return embeddings, llm

embeddings, llm = load_models()

if 'documents' in st.session_state and len(st.session_state.documents) > 0:
    with st.spinner('Processing documents..'):
        vs_data = st.session_state.vector_store
        if vs_data['type'] == 'pinecone':
            vector_store = Pinecone.from_documents(
                st.session_state.documents, embeddings, index_name=vs_data['name']
            )
        elif vs_data['type'] == 'faiss':
            vector_store = FAISS.from_documents(
                st.session_state.documents, embeddings, 
            )

    memory = ConversationTokenBufferMemory(
        max_token_limit=300, return_messages=True, 
        llm=llm, memory_key='chat_history'
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm, vector_store.as_retriever(), 
        chain_type='stuff', memory=memory, verbose=True
    )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything!"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner('Retrieving information..'):
                response = qa_chain.run(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning('Ingest at least one document first.')
