import uuid
import boto3
import boto3.exceptions
from BaseAWSService import BaseAWSService

class Route53Service(BaseAWSService):
    def __init__(self):
        super().__init__('route53')


    # Create hosted zone
    def create_zone(self, zone_name):
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
            print(f"hostedzone id: {zone_id}")
            self.add_tags_to_hosted_zone(zone_id)
        except boto3.exceptions.Boto3Error as e:
            print(f"Error while creating zone :( :{e} ")

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
            print(f"Tags added successfully to hosted zone {zone_id}")
        except Exception as e:
            print(f"Error adding tags: {e}")


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
            print(f"Record {record_name} created successfully!")
        except Exception as e:
            print(f"Failed to create record: {e}")

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
        return matching_zones

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
                print("Record updated successfully!")
            except Exception as e:
                print(f"Failed to update record: {e}")
        else:
            print("Please enter a valid zone_id.")

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
                print("Record deleted successfully!")
            except Exception as e:
                print(f"Failed to delete record: {e}")
        else:
            print("Please enter a valid zone_id.")

    # List records
    def list_resource_records(self, zone_id):
        response = self.client.list_resource_record_sets(HostedZoneId=zone_id)
        for record in response['ResourceRecordSets']:
            name = record.get('Name', 'N/A')
            record_type = record.get('Type', 'N/A')
            ttl = record.get('TTL', 'N/A')
            values = ', '.join([r['Value'] for r in record.get('ResourceRecords', [])])

            print(f"Name: {name}")
            print(f"Type: {record_type}")
            print(f"TTL: {ttl}")
            print(f"Values: {values}")
            print("-" * 50)