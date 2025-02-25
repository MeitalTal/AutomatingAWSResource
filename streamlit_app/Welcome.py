import streamlit as st
from modules.AWSAuthService import AWSAuthService

st.set_page_config(
    page_title="Automating AWS",
    page_icon="☁️",
    layout="wide"
)

aws_auth = AWSAuthService()
authenticated_user = aws_auth.get_authenticated_user()

# get AWS credentials username
if "username" not in st.session_state:
    st.session_state.username = authenticated_user if "Error" not in authenticated_user else ""

st.write("# Welcome to Automating AWS! ☁️")

if st.session_state.username:
    st.success(f"Welcome {st.session_state.username}!")
    st.write("Select a service from the sidebar to proceed.")

# If no AWS credentials are found
else:
    st.error("No AWS credentials found. Please configure AWS CLI using 'aws configure'.")

