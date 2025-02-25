import boto3
from botocore.exceptions import NoCredentialsError, ClientError

class AWSAuthService:
    def __init__(self):
        self.sts_client = boto3.client("sts")

    # check if you did aws configure
    def get_authenticated_user(self):
        try:
            identity = self.sts_client.get_caller_identity()
            arn = identity.get("Arn")
            username = arn.split("/")[-1]
            return username
        except NoCredentialsError:
            return "No AWS credentials found. Run 'aws configure'."
        except ClientError as e:
            return f"Error: {e}"
