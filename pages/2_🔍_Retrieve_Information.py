import streamlit as st
import openai

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from langchain.chains import ConversationalRetrievalChain


st.set_page_config('Retrieve Information', '🔍')
st.title('Retrieve Information 🔍')

if 'vector_store' in st.session_state:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    openai.api_key = st.secrets['OPENAI_API_KEY']
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)

    memory = ConversationTokenBufferMemory(
        max_token_limit=300, return_messages=True, 
        llm=llm, memory_key='chat_history'
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm, st.session_state.vector_store.as_retriever(), 
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
    st.warning('Connect your Pinecone DB first! ')
