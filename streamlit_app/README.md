# Streamlit App For Automating AWS
A Streamlit-based app to automate and manage AWS services like EC2 S3 and Route 53. Users can list create update and delete AWS records and instances through a simple web interface.

# Features
- User Authentication: Users enter their AWS username to log in.

- EC2 Instance Management: Create EC2 instance, list instances and manage instances (Start, stop, and reboot instances)

- Route 53 Management: Create, List hosted zones and record, manage records(Create, update, and delete records).

- S3 Management: Create Bucket, List Buckets and Upload file to Bucket.

# Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.8+
- Pip
- AWS CLI configured with credentials

### Clone the Repository

```bash
 git clone https://github.com/meitaltal/AutomatingAWSResource.git
 
 cd AutomatingAWSResource/AutomatingAWSStreamlitApp/
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

# Usage

### Run the Application

```bash
streamlit run streamlit_app/Welcome.py
```

### Login

- Enter your AWS username.

### Managing AWS Services

- Select a service from the sidebar.

- Select an Action from the sidebar.

- Follow on-screen instructions to manage AWS resource.

# Video Demo
[![Watch the video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://github.com/yourusername/yourrepo/blob/main/videos/demo.mp4)