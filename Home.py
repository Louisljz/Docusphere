import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access the environment variable
streamlit_server_max_upload_size = int(os.getenv("STREAMLIT_SERVER_MAX_UPLOAD_SIZE", default=1000))
st.set_page_config('Home', '📖')
st.title('Docusphere HomePage 📖')
