import json
from .BaseAWSService import BaseAWSService
import boto3
import boto3.exceptions
from botocore.exceptions import ClientError
import logging
import os
import streamlit as st
import pandas as pd



class S3Service(BaseAWSService):
    def __init__(self):
        super().__init__('s3')

    # Create S3 Buckets
    def create_bucket(self, bucket_name, acl):
        try:
            response = self.client.create_bucket(
                Bucket = bucket_name,
            )
            st.success(f"S3 bucket '{bucket_name}' created successfully")
            self.add_bucket_tags(bucket_name)
            # public access to the buckets
            if acl == "public":
                self.client.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': False,
                        'IgnorePublicAcls': False,
                        'BlockPublicPolicy': False,
                        'RestrictPublicBuckets': False
                    }
                )
                # Config Bucket Policy
                bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "PublicReadGetObject",
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{bucket_name}/*"
                        }
                    ]
                }
                # Update Bucket Policy
                self.client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=json.dumps(bucket_policy)
                )
                st.success(f"Bucket {bucket_name} created and set to public-read")

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code in ["BucketAlreadyExists", "BucketAlreadyOwnedByYou"]:
                st.error(f"The bucket name '{bucket_name}' is already in use. Please choose a different name.")
            else:
                st.error(f"Error while creating bucket: {e}")


    # Add tags when creating S3 bucket
    def add_bucket_tags(self, bucket_name):
        try:
            tags = {
                'TagSet': [
                    {'Key': 'Owner', 'Value': self.username},
                    {'Key': 'CreateBy', 'Value': "CLI"}
                ]
            }
            self.client.put_bucket_tagging(Bucket=bucket_name, Tagging=tags)

        except boto3.exceptions.Boto3Error as e:
            st.error(f"Failed to add tags: {e}")

    # list of filtered buckets by tags
    def buckets(self):
        try:
            response = self.client.list_buckets()
            buckets_with_tags = []

            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                try:
                    tag_response = self.client.get_bucket_tagging(Bucket=bucket_name)
                    tags = tag_response['TagSet']
                    has_required_tags = False
                    for tag in tags:
                        if tag['Key'] == "CreateBy" and tag['Value'] == "CLI":
                            for tag in tags:
                                if tag['Key'] == "Owner" and tag['Value'] == self.username:
                                    has_required_tags = True
                                    break
                        if has_required_tags:
                            buckets_with_tags.append(bucket_name)
                            break

                except ClientError as e:
                    if e.response['Error']['Code'] == 'NoSuchTagSet':
                        continue

            return buckets_with_tags
        except boto3.exceptions.Boto3Error as e:
            st.error(f"Error listing buckets: {e}")
            return []

    # Upload file
    def upload_file(self, file_path, bucket_name):
        object_name = os.path.basename(file_path)

        for bucket in self.buckets():
            if bucket == bucket_name:
                # Upload the file
                try:
                    response = self.client.upload_file(file_path, bucket_name, object_name)
                    st.success(f"The file is uploaded :) ")
                except ClientError as e:
                    logging.error(e)
                    st.error(f"Failed to upload the file :(  ")


    # Print list of buckets
    def list_of_buckets(self):
        buckets = self.buckets()
        if not buckets:
            st.error("No buckets found with the required tags.")
        else:
            buckets_data = []
            for bucket in buckets:
                buckets_data.append({"Bucket Name": bucket})
            if buckets_data:
                df = pd.DataFrame(buckets_data)
                df.index = range(1, len(df) + 1)
                st.dataframe(df)
