from fastapi import FastAPI
from modules.EC2Service import EC2Service
from modules.S3Service import S3Service
from modules.Route53Service import Route53Service
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

VALID_INSTANCE_TYPE = ("t3.nano","t4g.nano")
VALID_AMI = ("Ubuntu", "Amazon Linux")
VALID_ACL = ("public","private")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is running now!"}


# EC2
ec2 = EC2Service()

# List instances
@app.get("/ec2/list-instances")
def list_instances():
    return ec2.print_list_of_instances()

# Create EC2 instance
@app.post("/ec2/create-instance")
def create_instance(instance_name: str, instance_type: str, instance_ami: str):
    if instance_ami not in VALID_AMI:
        return {"error": f"Invalid AMI. Choose from {VALID_AMI}"}
    if instance_type not in VALID_INSTANCE_TYPE:
        return {"error": f"Invalid instance type. Choose from {VALID_INSTANCE_TYPE}"}

    ec2.create_instance(instance_name, instance_type, instance_ami)
    return {"message": "Instance created successfully!"}

# start/stop/reboot instance
@app.post("/ec2/manage-instance")
def manage_instance(instance_id: str, action: str):
    if action not in ["start", "stop", "reboot"]:
        return {"error": "Invalid action. Choose from start, stop, reboot."}

    ec2.manage_instance(instance_id, action)
    return {"message": f"Instance {action}ed successfully!"}

# S3
s3 = S3Service()

# List Buckets
@app.get("/s3/list-buckets")
def list_buckets():
    return s3.list_of_buckets()

# Create Bucket
@app.post("/s3/create-bucket")
def create_bucket(bucket_name: str, bucket_acl: str, confirm: bool = False):
    if bucket_acl not in VALID_ACL:
        return {"error": f"Invalid ACL. Choose from {VALID_ACL}"}

    if bucket_acl == "public" and not confirm:
        return {"warning": f"Are you sure you want to set bucket '{bucket_name}' as PUBLIC? Please resend request with 'confirm=true'."}

    s3.create_bucket(bucket_name, bucket_acl)
    return {"message": f"Bucket '{bucket_name}' created successfully!"}

# Upload file to bucket
@app.post("/s3/upload-file")
def create_bucket(bucket_name: str, file_path: str):
    s3.upload_file(file_path, bucket_name)
    return {"message": f"File uploaded successfully to '{bucket_name}'!"}


# Route 53
r53 = Route53Service()

# List zones
@app.get("/route53/list-zones")
def list_zones():
    return r53.list_hosted_zone_by_tags()

# Create Zone
@app.post("/route53/create-zone")
def create_zone(zone_name: str):
    r53.create_zone(zone_name)
    return {"message": f"Zone '{zone_name}' created successfully!"}

# List Records By Zone
@app.get("/route53/list-records")
def list_records(zone_id: str):
    return {"records": r53.list_resource_records(zone_id)}

# Create Record
@app.post("/route53/create-record")
def create_record(zone_id: str, record_name: str, value: str, ttl: int):
    r53.create_dns_resource_record(zone_id, record_name, value, ttl)
    return {"message": f"Record {record_name} created successfully!"}

# Update Record
@app.put("/route53/update-record")
def update_record(zone_id: str, record_name: str, value: str, ttl: int):
    r53.update_resource_record(zone_id, record_name, value, ttl)
    return {"message": f"Record '{record_name}' updated successfully in zone '{zone_id}'!"}

# Delete Record
@app.delete("/route53/delete-record")
def delete_record(zone_id: str, record_name: str, value: str, ttl: int):
    r53.delete_resource_record(zone_id, record_name, value, ttl)
    return {"message": f"Record '{record_name}' deleted successfully from zone '{zone_id}'!"}