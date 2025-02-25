import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.modules.S3Service import S3Service


def main():
    # Checks whether the user is logged in
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("Sorry, You need to login first 🔑")
        st.stop()


    service_class = S3Service()
    st.title("S3 Management")
    action = st.sidebar.selectbox("Select an Action:", ["None", "Create Bucket","List Buckets", "Upload File"])

    if action == "None":
        st.write("Select a action from the sidebar to proceed.")

    # Create Bucket
    elif action == "Create Bucket":
        st.subheader("Create S3 Bucket")
        bucket_name = st.text_input("Enter Bucket name:")
        acl = st.selectbox("Enter ACL:", ["public","private"])
        if acl == "public":
            confirm = st.radio("Are you sure?", ("yes", "no"))
            if confirm != "yes":
                acl = "private"
        if st.button("Create"):
            service_class.create_bucket(bucket_name, acl)

    # List Buckets
    elif action == "List Buckets":
        st.subheader("List of Buckets")
        service_class.list_of_buckets()
    # Upload file
    else:
        st.subheader("Upload File")
        buckets = service_class.buckets()
        if not buckets:
            st.error("No user-created buckets found.")
            st.stop()
        selected_bucket = st.selectbox("Select bucket name:", buckets)
        file_path = st.text_input("Enter file path: ")
        if st.button("Upload File"):
            service_class.upload_file(file_path, selected_bucket)

main()