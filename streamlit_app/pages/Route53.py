import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from streamlit_app.modules.Route53Service import Route53Service


def main():

    # Checks whether the user is logged in
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("Sorry, You need to login first 🔑")
        st.stop()

    service_class = Route53Service()
    st.title("Route53 Management")
    action = st.sidebar.selectbox("Select an Action:", ["None", "Create Hosted Zone","List Hosted Zone", "List Records" ,"Create Record", "Update Record", "Delete Record"])

    if action == "None":
        st.write("Select a action from the sidebar to proceed.")

    # Create Hosted Zone
    elif action == "Create Hosted Zone":
        st.subheader("Create Hosted Zone")
        zone_name = st.text_input("Enter Zone name: ")
        if st.button("Create"):
            service_class.create_zone(zone_name)

    # List Hosted Zone
    elif action == "List Hosted Zone":
        st.subheader("List Hosted Zone")
        service_class.print_list_hosted_zone()

    # List Records
    elif action == "List Records":
        st.subheader("List Records")
        hosted_zones = service_class.list_hosted_zone_by_tags()
        selected_zone_id = st.selectbox("Select Hosted Zone ID:", hosted_zones)
        if st.button("Get List of Records"):
            service_class.list_resource_records(selected_zone_id)

    # Create Record
    elif action == "Create Record":
        st.subheader(action)
        hosted_zones = service_class.list_hosted_zone_by_tags()
        if not hosted_zones:
            st.error("No hosted zones found. Please create a hosted zone first.")
            st.stop()
        selected_zone_id = st.selectbox("Select Hosted Zone ID:", hosted_zones)
        record_name = st.text_input("Enter record name (end with the hosted zone name!):")
        value = st.text_input("Enter value:")
        ttl = int(st.number_input("Enter TTL (seconds):", min_value=60, max_value=172800, value=60, step=10))
        if st.button(action):
            service_class.create_dns_resource_record(selected_zone_id, record_name, value, ttl)

    # Update or delete Record
    else:
        st.subheader(action)
        # Get combobox of zones
        hosted_zones = service_class.list_hosted_zone_by_tags()
        if not hosted_zones:
            st.error("No hosted zones found. Please create a hosted zone first.")
            st.stop()
        selected_zone_id = st.selectbox("Select Hosted Zone ID:", hosted_zones)

        # Get combobox of records
        records = service_class.list_user_records(selected_zone_id)
        if not records:
            st.error("No user-created records found in this zone.")
            st.stop()

        selected_record_name = st.selectbox("Select Record Name:", list(records.keys()))

        # Get record data
        selected_record_data = records[selected_record_name][0]
        current_value = selected_record_data.get("Values")
        current_ttl = selected_record_data.get("TTL")

        # Update Record
        if action == "Update Record":
            new_value = st.text_input("Enter new value:", value=current_value)
            new_ttl = st.number_input("Enter TTL (seconds):", min_value=60, max_value=172800, value=int(current_ttl),step=10)

            if st.button("Update Record"):
                service_class.update_resource_record(selected_zone_id, selected_record_name, new_value, new_ttl)

        # Delete Record
        else:
            if st.button("Delete Record"):
                service_class.delete_resource_record(selected_zone_id, selected_record_name, current_value, int(current_ttl))

main()
