import streamlit as st

if "documents" not in st.session_state:
    st.session_state.documents = []

st.set_page_config('Home', '📖')
st.title('Docusphere HomePage 📖')
