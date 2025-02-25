import uuid
import boto3
import boto3.exceptions
from .BaseAWSService import BaseAWSService
import streamlit as st
import pandas as pd

class Route53Service(BaseAWSService):
    def __init__(self):
        super().__init__('route53')


    # Create hosted zone
    def create_zone(self, zone_name, ):
        try:
            response = self.client.create_hosted_zone(
                Name = zone_name,
                VPC={
                    'VPCRegion': self.region,
                    'VPCId': 'vpc-0c66ad29a15f62553'
                },
                CallerReference = str(uuid.uuid4()),
            )
            zones = self.client.list_hosted_zones_by_name(DNSName=zone_name)
            zone_id = zones['HostedZones'][0]['Id'].split('/')[-1]
            st.success(f"hostedzone id: {zone_id}")
            self.add_tags_to_hosted_zone(zone_id)
        except boto3.exceptions.Boto3Error as e:
            st.error(f"Error while creating zone :(  : {e}")

    # Add Tags - Owner and CLI
    def add_tags_to_hosted_zone(self, zone_id):
        tagging_client = boto3.client('resourcegroupstaggingapi')
        tags = [
            {'Key': 'Owner', 'Value': self.username},
            {'Key': 'CreateBy', 'Value': "CLI"}
            ]
        try:
            response = tagging_client.tag_resources(
                ResourceARNList=[f'arn:aws:route53:::hostedzone/{zone_id}'],
                Tags={tag['Key']: tag['Value'] for tag in tags}
            )
            st.success(f"Tags added successfully to hosted zone {zone_id}")
        except Exception as e:
            st.error(f"Error adding tags: {e}")


    # Create Record
    def create_dns_resource_record(self, zone_id, record_name, value, ttl=60):
        if not record_name.endswith('.'):
            record_name += '.'
        try:
            response = self.client.change_resource_record_sets(
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'ResourceRecords': [
                                    {
                                        'Value': value,
                                    },
                                ],
                                'TTL': ttl,
                                'Type': 'A',
                            },
                        },
                    ],
                },
                HostedZoneId=zone_id,
            )
            st.success(f"Record {record_name} created successfully!")
        except Exception as e:
            st.error(f"Failed to create record: {e}")

    # List hosted zones
    def list_hosted_zone_by_tags(self):
        response = self.client.list_hosted_zones()

        matching_zones = []

        for zone in response['HostedZones']:
            zone_id = zone['Id'].split("/")[-1]

            tags_response = self.client.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=zone_id
            )

            for tag in tags_response['ResourceTagSet']['Tags']:
                if tag['Key'] == "CreateBy" and tag['Value'] == "CLI":
                    for tag in tags_response['ResourceTagSet']['Tags']:
                        if tag['Key'] == "Owner" and tag['Value'] == self.username:
                            matching_zones.append(zone_id)
        if matching_zones:
            return matching_zones
        else:
            return []

    # print List hosted zones
    def print_list_hosted_zone(self):
        zone_data = []
        for zone_id in self.list_hosted_zone_by_tags():
            hosted_zone = self.client.get_hosted_zone(Id=zone_id)
            zone_name = hosted_zone["HostedZone"]["Name"]
            zone_data.append({"Hosted Zone Name": zone_name, "Hosted Zone ID": zone_id})

        if zone_data:
            df = pd.DataFrame(zone_data)
            st.table(df.set_index("Hosted Zone Name"))
        else:
            st.warning("No matching hosted zones found.")



    # Update record
    def update_resource_record(self, zone_id, record_name, value, ttl=60):
        if zone_id in self.list_hosted_zone_by_tags():
            try:
                response = self.client.change_resource_record_sets(
                    ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'UPSERT',
                                'ResourceRecordSet': {
                                    'Name': record_name,
                                    'ResourceRecords': [
                                        {
                                            'Value': value,
                                        },
                                    ],
                                    'TTL': ttl,
                                    'Type': 'A',
                                },
                            },
                        ],
                    },
                    HostedZoneId=zone_id,
                )
                st.success("Record updated successfully!")
            except Exception as e:
                st.error(f"Failed to update record: {e}")
        else:
            st.error("Please enter a valid zone_id.")

    # Delete DNS resource
    def delete_resource_record(self,zone_id, record_name, value, ttl=60):
        if zone_id in self.list_hosted_zone_by_tags():
            try:
                response = self.client.change_resource_record_sets(
                    ChangeBatch={
                        'Changes': [
                            {
                                'Action': 'DELETE',
                                'ResourceRecordSet': {
                                    'Name': record_name,
                                    'ResourceRecords': [
                                        {
                                            'Value': value,
                                        },
                                    ],
                                    'TTL': ttl,
                                    'Type': 'A',
                                },
                            },
                        ],
                    },
                    HostedZoneId=zone_id,
                )
                st.success("Record deleted successfully!")
            except Exception as e:
                st.error(f"Failed to delete record: {e}")
        else:
            st.error("Please enter a valid zone_id.")



    # List records
    def list_resource_records(self, zone_id):
        response = self.client.list_resource_record_sets(HostedZoneId=zone_id)
        record_data = []
        for record in response['ResourceRecordSets']:
            name = record.get('Name', 'N/A')
            record_type = record.get('Type', 'N/A')
            ttl = record.get('TTL', 'N/A')
            values = ', '.join([r['Value'] for r in record.get('ResourceRecords', [])])

            st.markdown(f"### Record: {name}")
            st.markdown(f"**Type**: {record_type}")
            st.markdown(f"**TTL**: {ttl}")
            st.markdown(f"**Values**: {values}")
            st.markdown("-" * 50)

    def list_user_records(self, zone_id):
        try:
            response = self.client.list_resource_record_sets(HostedZoneId=zone_id)
            records = {}

            for record in response['ResourceRecordSets']:
                record_name = record.get('Name', '').strip()
                record_type = record.get('Type', 'N/A')
                ttl = record.get('TTL', 'N/A')
                values = ', '.join([r['Value'] for r in record.get('ResourceRecords', [])])
                if record_name and record_type == 'A':
                    records[record_name] = [{
                        "TTL": ttl,
                        "Values": values
                    }]

            if records:
                return records
            else:
                return {}

        except Exception as e:
            st.error(f"Error with getting records: {e}")
            return {}
