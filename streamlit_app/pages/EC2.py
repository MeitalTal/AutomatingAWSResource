import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.modules.EC2Service import EC2Service

def main():
    # Checks whether the user is logged in
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("Sorry, You need to login first 🔑")
        st.stop()

    service_class = EC2Service()
    st.title("EC2 Management")
    action = st.sidebar.selectbox("Select an Action:", ["None", "Create Instance","List Instances", "Start Instance", "Stop Instance", "Reboot Instance"])

    if action == "None":
        st.write("Select a action from the sidebar to proceed.")

    # Create Instance
    elif action == "Create Instance":
        st.subheader("Create EC2 Instance")
        instance_name = st.text_input("Enter Instance name:")
        instance_type = st.selectbox("Enter Instance Type:", ["t3.nano","t4g.nano"])
        instance_ami = st.selectbox("Enter Instance ID:", ["Ubuntu", "Amazon Linux"])
        if st.button("Start"):
            st.warning(f"Instance {instance_name} is Lunching...")
            service_class.create_instance(instance_name, instance_type, instance_ami)

    # List instances
    elif action == "List Instances":
        st.subheader("List of your Instances")
        service_class.print_list_of_instances()

    # Stat instance
    elif action == "Start Instance":
        st.subheader("Start Instance")
        stopped_instances = service_class.list_of_instances_by_state("stopped")
        if not stopped_instances:
            st.error("No user-created stopped instances")
            st.stop()
        instance_name = st.selectbox("Select instance name:", list(stopped_instances.keys()))
        instance_id = stopped_instances[instance_name]
        if st.button("Start"):
            service_class.manage_instance(instance_id, "start")

    # Stop Instance
    elif action == "Stop Instance":
        st.subheader("Stop Instance")
        running_instances = service_class.list_of_instances_by_state("running")
        if not running_instances:
            st.error("No user-created running instances")
            st.stop()
        instance_name = st.selectbox("Select instance name:", list(running_instances.keys()))
        instance_id = running_instances[instance_name]
        if st.button("Stop"):
            service_class.manage_instance(instance_id, "stop")

    # Reboot Instance
    else:
        st.subheader("Reboot Instance")
        running_instances = service_class.list_of_instances_by_state("running")
        if not running_instances:
            st.error("No user-created running instances")
            st.stop()
        instance_name = st.selectbox("Select instance name:", list(running_instances.keys()))
        instance_id = running_instances[instance_name]
        if st.button("Reboot"):
            service_class.manage_instance(instance_id, "reboot")

main()