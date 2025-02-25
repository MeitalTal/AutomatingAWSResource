import boto3
from modules.AWSAuthService import AWSAuthService

class BaseAWSService:
    def __init__(self, service_name):
        self.service_name = service_name
        self.region = "us-east-1"
        auth_service = AWSAuthService()
        self.username = auth_service.get_authenticated_user().split("/")[-1]

        session = boto3.Session()
        if service_name == 'ec2':
            self.client = session.resource(self.service_name, self.region)
        else:
            self.client = session.client(self.service_name, self.region)