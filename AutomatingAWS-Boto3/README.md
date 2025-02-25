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
 
 cd AutomatingAWSResource/AutomatingAWS-Boto3
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

```bash
 python main.py
```

- Enter your AWS username.

##### Managing AWS Services

- Select a service.

- Select an Action.

- Follow on-screen instructions to manage AWS resource.

#### Demo
![Demo GIF](assets/demo.gif)

