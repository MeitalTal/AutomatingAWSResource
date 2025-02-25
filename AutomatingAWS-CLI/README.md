# AWS Automation CLI 
A command-line tool to automate and manage AWS services like EC2, S3, and Route 53.

# Features
- User Authentication: Users enter their AWS username to log in.

- EC2 Instance Management: Create EC2 instance, list instances and manage instances (Start, stop, and reboot instances)

- Route 53 Management: Create, List hosted zones and records, manage records(Create, update, and delete records).

- S3 Management: Create Bucket, List Buckets and Upload file to Bucket.

# Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Pip
- AWS CLI configured with credentials

### Clone the Repository

```bash
 git clone https://github.com/MeitalTal/AutomatingAWSResource.git
 
 cd AutomatingAWSResource/AutomatingAWS-CLI
```

### Install Dependencies
```bash
 pip install -r requirements.txt
```

# Usage

### Authenticate
Before using, make sure you are logged in with AWS CLI:
```bash
 aws configure
```

### Run the Application

### EC2 Management

#### List EC2 instances:
```bash
python main.py ec2 list
```

#### Create an EC2 instance:

```bash
python main.py ec2 create-instance --instance-name my-instance --instance-type t3.nano --instance-ami "Ubuntu"
```

#### Start, Stop, Reboot an EC2 instance:

```bash
    python main.py ec2 start --instance-id i-xxxx 
    python main.py ec2 stop --instance-id i-xxxx
    python main.py ec2 reboot --instance-id i-xxxx
```

### S3 Bucket Management

#### List S3 buckets:

```bash
python main.py s3 list-buckets
```

#### Create an S3 bucket:
```bash
python main.py s3 create-bucket --bucket-name my-bucket --bucket-acl public
```
   - If setting ACL to public, you'll be asked to confirm.

#### Upload a file to an S3 bucket:

```bash
python main.py s3 upload-file --bucket-name my-bucket --file-path <file-path>
```

### Route 53 DNS Management

#### List hosted zones:

```bash
python main.py route53 list-zones
```

#### Create a new hosted zone:

```bash
python main.py route53 create-zone --zone-name example.com
```

#### List DNS records in a hosted zone:

```bash
python main.py route53 list-records --zone-id <zone-id>
```

#### Create, Update, Delete a DNS record:

```bash
python main.py route53 create-record --zone-id <zone-id> --record-name www.example.com --value "192.168.1.1" --ttl 300
python main.py route53 update-record --zone-id <zone-id> --record-name www.example.com --value "192.168.1.2" --ttl 300
python main.py route53 delete-record --zone-id <zone-id> --record-name www.example.com --value "192.168.1.2" --ttl 300
```

