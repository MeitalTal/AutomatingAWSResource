import argparse
from modules.EC2Service import EC2Service
from modules.S3Service import S3Service
from modules.Route53Service import Route53Service
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

VALID_INSTANCE_TYPE = ("t3.nano","t4g.nano")
VALID_AMI = ("Ubuntu", "Amazon Linux")
VALID_ACL = ("public","private")


def main():
    parser = argparse.ArgumentParser(description="AWS CLI Tool for EC2, S3, and Route 53")

    subparsers = parser.add_subparsers(dest="service", required=True)

    # EC2 Commands
    ec2_parser = subparsers.add_parser("ec2", help="Manage EC2 instances")
    ec2_parser.add_argument("action", choices=["create-instance","start", "stop", "reboot", "list"], help="EC2 action")
    ec2_parser.add_argument("--instance-name", help="EC2 instance name (required for creating instance)")
    ec2_parser.add_argument("--instance-type", help="EC2 instance ID (required for creating instance)")
    ec2_parser.add_argument("--instance-ami", help="EC2 instance ID (required for creating instance)")
    ec2_parser.add_argument("--instance-id", help="EC2 instance ID (required for start/stop/reboot)")

    # S3 Commands
    s3_parser = subparsers.add_parser("s3", help="Manage S3 Buckets")
    s3_parser.add_argument("action", choices=["create-bucket", "list-buckets", "upload-file"], help="S3 action")
    s3_parser.add_argument("--bucket-name", help="S3 bucket name (required for create-bucket/upload-file)")
    s3_parser.add_argument("--bucket-acl", help="S3 bucket acl (required for create-bucket)")
    s3_parser.add_argument("--file-path", help="File path for upload (required for upload-file)")

    # Route 53 Commands
    r53_parser = subparsers.add_parser("route53", help="Manage Route 53 DNS Records")
    r53_parser.add_argument("action", choices=["create-zone" ,"create-record", "update-record", "delete-record", "list-records", "list-zones"], help="Route 53 action")
    r53_parser.add_argument("--zone-name", help="Record name (required for create-zone)")
    r53_parser.add_argument("--zone-id", help="Hosted Zone ID (required for create-record/update-record/delete-record/list-records)")
    r53_parser.add_argument("--record-name", help="Record name (required for create/update/delete)")
    r53_parser.add_argument("--value", help="Record value (required for create/update)")
    r53_parser.add_argument("--ttl", type=int, help="TTL value (required for create/update)")

    args = parser.parse_args()

    # EC2
    if args.service == "ec2":
        ec2 = EC2Service()

        # List instances
        if args.action == "list":
            ec2.print_list_of_instances()

        # Create EC2 instance
        elif args.action == "create-instance":
            if not args.instance_ami or not args.instance_type or not args.instance_name:
                print("Error: --instance-ami, --instance-type, --instance-name are required for create-instance")
            else:
                if args.instance_ami not in VALID_AMI:
                    print(f"Error: '{args.instance_ami}' is not a valid record type. Please choose from {VALID_AMI}")
                    exit(1)
                if args.instance_type not in VALID_INSTANCE_TYPE:
                    print(f"Error: '{args.instance_type}' is not a valid record type. Please choose from {VALID_INSTANCE_TYPE}")
                    exit(1)
                ec2.create_instance(args.instance_name, args.instance_type, args.instance_ami)

        # start/stop/reboot instance
        elif args.instance_id:
            if args.action not in ["start", "stop", "reboot"]:
                print("Error: Invalid action. Choose from start, stop, reboot.")
                exit(1)
            ec2.manage_instance(args.instance_id, args.action)
        else:
            print("Error: Missing required arguments for EC2")


    # S3 Logic
    elif args.service == "s3":
        s3 = S3Service()
        if args.action == "list-buckets":
            s3.list_of_buckets()
        elif args.action == "create-bucket" and args.bucket_name and args.bucket_acl:
            if args.bucket_acl not in VALID_ACL:
                print(f"Error: '{args.bucket_acl}' is not a valid record type. Please choose from {VALID_ACL}")
                exit(1)

            if args.bucket_acl == "public":
                confirmation = input(f"Are you sure you want to set bucket '{args.bucket_name}' as PUBLIC? (yes/no): ").strip().lower()
                if confirmation != "yes":
                    args.bucket_acl = "private"
            s3.create_bucket(args.bucket_name, args.bucket_acl)
        elif args.action == "upload-file" and args.bucket_name and args.file_path:
            s3.upload_file(args.file_path, args.bucket_name)
        else:
            print("Error: Missing required arguments for S3")

    # Route 53 Logic
    elif args.service == "route53":
        r53 = Route53Service()
        if args.action == "list-zones":
            print(r53.list_hosted_zone_by_tags())
        elif args.action == "create-zone" and args.zone_name:
            r53.create_zone(args.zone_name)
        elif args.action == "list-records" and args.zone_id:
            r53.list_resource_records(args.zone_id)
        elif args.action in ["create-record", "update-record", "delete-record"] and args.zone_id and args.record_name:
            if not args.value or not args.ttl:
                print("Error: --value, and --ttl are required for this action")
            else:
                if args.action == "create-record":
                    r53.create_dns_resource_record(args.zone_id, args.record_name, args.value, args.ttl)
                elif args.action == "update-record":
                    r53.update_resource_record(args.zone_id, args.record_name, args.value, args.ttl)
                elif args.action == "delete-record":
                    r53.delete_resource_record(args.zone_id, args.record_name, args.value, args.ttl)

main()