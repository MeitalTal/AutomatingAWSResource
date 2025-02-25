# AWS Management API using FastAPI

### Overview

This project provides a FastAPI-based RESTful API for managing AWS services, including EC2, S3, and Route 53. It allows developers to list, create, update, and delete AWS resources via HTTP requests.

### Features

- EC2 Management: List instances, create instances, start/stop/reboot instances.

- S3 Management: List buckets, create buckets (with public ACL confirmation), upload files.

- Route 53 Management: List hosted zones, create zones, manage DNS records.

### Prerequisites

Before running the API, ensure you have:

- Python 3.7+

- AWS credentials configured

### Installation

1. Clone the repository:

```sh
git clone https://github.com/MeitalTal/AutomatingAWSResource.git
cd AutomatingAWSResource/AutomatingAWSFastAPI
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Set up AWS credentials:
```sh
aws configure
```

### Running the API

Start the FastAPI server using:

```sh
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```
The API will be available at: http://127.0.0.1:8000

### API Endpoints

##### EC2:

- List Instances: `GET /ec2/list-instances`

- Create Instance: `POST /ec2/create-instance?instance_name={name}&instance_type={type}&instance_ami={ami}`

- Manage Instance: `POST /ec2/manage-instance?instance_id={id}&action={start|stop|reboot}`

##### S3:

- List Buckets: `GET /s3/list-buckets`

- Create Bucket: `POST /s3/create-bucket?bucket_name={name}&bucket_acl={public|private}&confirm={true|false}`

- Upload File: `POST /s3/upload-file?bucket_name={name}&file_path={path}`

##### Route 53:

- List Hosted Zones: `GET /route53/list-zones`

- Create Zone: `POST /route53/create-zone?zone_name={name}`

- List Records: `GET /route53/list-records?zone_id={id}`

- Create Record: `POST /route53/create-record?zone_id={id}&record_name={name}&value={value}&ttl={ttl}`

- Update Record: `PUT /route53/update-record?zone_id={id}&record_name={name}&value={value}&ttl={ttl}`

- Delete Record: `DELETE /route53/delete-record?zone_id={id}&record_name={name}&value={value}&ttl={ttl}`


### Testing
You can test the API using Swagger UI: http://127.0.0.1:8000/docs

### Deployment

To deploy this API you need to host it on EC2:

- Launch an EC2 Instance (make sure you open port 8000 (FastAPI) when you configured the security group
- Install Dependencies on EC2:
```sh
sudo dnf update
sudo dnf install python3
sudo pip3 install fastapi uvicorn boto3
```

- Clone Your Project & Run FastAPI:
```sh
git clone https://github.com/meitaltal/AWS-Management-API.git
cd AWS-Management-API
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

- Access Your API:
```sh
http://ec2-ip:8000
```
