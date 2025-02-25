from .BaseAWSService import BaseAWSService
import streamlit as st
import pandas as pd


class EC2Service(BaseAWSService):
    def __init__(self):
        super().__init__('ec2')

    # Filter instances
    def instances(self):
        instances = self.client.instances.filter(
            Filters=[{'Name': 'tag:Owner', 'Values': [self.username]},
                       {'Name': 'tag:CreateBy', 'Values': ['CLI']}])
        return instances

    def count_of_running_instance(self):
        count_instances = 0
        for instance in self.instances():
            if instance.state['Name'] == "running":
                count_instances+=1
        return count_instances


    # Create EC2 instance
    def create_instance(self, instance_name, instance_type, ami):

        ami_map = {
            ("t3.nano", "Ubuntu"): "ami-04b4f1a9cf54c11d0",
            ("t3.nano", "Amazon Linux"): "ami-053a45fff0a704a47",
            ("t4g.nano", "Ubuntu"): "ami-0a7a4e87939439934",
            ("t4g.nano", "Amazon Linux"): "ami-0c518311db5640eff",
        }
        ami = ami_map.get((instance_type, ami),)

        if self.count_of_running_instance() < 2:
            try:
                response = self.client.create_instances(
                    ImageId=ami,
                    InstanceType=instance_type,
                    KeyName="MeitalTal-KeyPair",
                    MinCount=1,
                    MaxCount=1,
                    NetworkInterfaces =
                    [ {
                        'DeviceIndex': 0,
                        'SubnetId': 'subnet-0296344e0e121adae',
                        'Groups': ['sg-00545de552c77b5e7'],
                        'AssociatePublicIpAddress': True,
                    } ],
                    TagSpecifications=[
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': self.username + '-' + instance_name
                                },
                                {
                                    'Key': 'Owner',
                                    'Value': self.username
                                },
                                {
                                    'Key': 'CreateBy',
                                    'Value': "CLI"
                                },
                            ]
                        },
                    ],
                )
                launched_instance = response[0]
                launched_instance.wait_until_running()
                launched_instance.reload()
                st.success("The instant has been launched successfully!")
                st.write(f"Instance ID: {launched_instance.id}")
                st.write(f"Public IP: {launched_instance.public_ip_address}")
            except Exception as e:
                st.error(f"Error creating instance: {e}")
        else:
            st.error("Sorry! You can have just 2 running instances!")


    # Get List of Instances that created by CLI
    def print_list_of_instances(self):
        instances_data = []

        for instance in self.instances():
            instance_name = "Unknown"
            if instance.tags:
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break

            instances_data.append({
                "Instance Name": instance_name,
                "Instance ID": instance.id,
                "State": instance.state['Name']
            })

        if instances_data:
            df = pd.DataFrame(instances_data)
            df.index = range(1, len(df) + 1)
            st.table(df)
        else:
            st.warning("No instances found.")

    # Print list of instances by state
    def list_of_instances_by_state(self, state):
        instances_data = {}
        for instance in self.instances():
            instance_name = "Unknown"
            if instance.tags:
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break

            if instance.state['Name'] == state:
                instances_data[instance_name] =  instance.id

        if instances_data:
            return instances_data
        else:
            return {}



    # Start,stop or reboot instance by instance_id
    def manage_instance(self, instance_id, action):

        actions = {
            "start": "stopped",
            "stop": "running",
            "reboot": "running"
        }

        if action not in actions:
            st.warning("Invalid action.")
            return

        for instance in self.instances():
            if instance.state['Name'] == actions[action] and instance.id == instance_id:
                try:
                    method = getattr(instance, action)  # (start/stop/reboot)
                    method()
                    st.success(f"Instance {instance_id} is {action}ing...")
                except Exception as e:
                    st.error(f"Failed to {action} instance {instance_id}: {e}")
                return "Failed!"
        st.warning(f"Instance {instance_id} not found or not in '{actions[action]}' state.")