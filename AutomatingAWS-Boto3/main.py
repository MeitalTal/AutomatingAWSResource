from EC2Service import EC2Service
from Route53Service import Route53Service
from S3Service import S3Service


# get input and check if it is valid
def get_valid_input(prompt, valid_options):
    user_input = input(f"{prompt}: ")
    while user_input not in valid_options:
        print("Invalid choice, please try again.")
        user_input = input(f"{prompt}: ")
    return user_input


# get info from the developer and activate create_instance class function
def create_ec2_instance(service_class):
    list_of_instance_type = ("t3.nano","t4g.nano")
    list_of_ami = ("Ubuntu", "Amazon Linux")
    instance_name = input("Enter instance name: ")
    instance_type = get_valid_input(f"Select an instance type {list_of_instance_type}", list_of_instance_type)
    ami = get_valid_input(f"Select an AMI {list_of_ami}", list_of_ami)
    print("Trying to lunch the instance, please wait :) ")
    service_class.create_instance(instance_name,instance_type, ami)

# get info from the developer and activate create_bucket class function
def create_s3_bucket(service_class):
    list_of_acl = ("public","private")
    bucket_name = input(f"Select name for the bucket: ").lower().strip()
    acl = get_valid_input(f"Select ACL {list_of_acl}: ", list_of_acl)
    if acl == "public":
        confirm = input("Are you sure? yes/no ").lower().strip()
        if confirm != "yes":
            acl = "private"
    service_class.create_bucket(bucket_name, acl)

# according to the developer choice, activate the function
def create_or_update_record(service_class, action, zone_id, record_name, value, ttl):
    if action == 'create':
        service_class.create_dns_resource_record(zone_id, record_name, value, ttl)
    elif action == 'update':
        service_class.update_resource_record(zone_id, record_name, value, ttl)
    elif action == 'delete':
        service_class.delete_resource_record(zone_id, record_name, value, ttl)

# main while
def main():
    services = {
        "1": {"name": "EC2 Service", "actions": {"1": "Launch EC2", "2": "Start instance", "3": "Stop instance", "4": "Reboot instance","5": "List instances"}},
        "2": {"name": "S3 Service ", "actions": {"1": "Create Bucket", "2": "Upload file", "3": "List Buckets"}},
        "3": {"name": "Route53 Service", "actions": {"1": "Create DNS Zone", "2": "Create Record", "3": "Update Record", "4": "Delete Record", "5": "List Hosted Zones", "6": "List Records"}},
        "4": {"name": "Exit", "actions": {None}}
    }

    while True:
        print("Services: ")
        for key, value in services.items():
            print(f"{key}. {value['name']}")

        service_choice = get_valid_input("Select a Service", services.keys())

        if service_choice == "4":
            print("See you later, Bye!")
            break

        service = services[service_choice]
        print(f"\n Select an action for {service['name']}:")
        for key, value in service['actions'].items():
            print(f"{key}. {value}")

        action_choice = get_valid_input("Enter selected action", service['actions'].keys())

        if service_choice == "1":
            service_class = EC2Service()
            if action_choice == "1":
                create_ec2_instance(service_class)
            elif action_choice == "2":
                instance_id = input("Enter instance id you wanna start: ")
                service_class.manage_instance(instance_id,"start")
            elif action_choice == "3":
                instance_id = input("Enter instance id you wanna stop: ")
                service_class.manage_instance(instance_id, "stop")
            elif action_choice == "4":
                instance_id = input("Enter instance id you wanna reboot: ")
                service_class.manage_instance(instance_id, "reboot")
            else:
                service_class.print_list_of_instances()

        elif service_choice == "2":
            service_class = S3Service()
            if action_choice == "1":
                create_s3_bucket(service_class)
            elif action_choice == "2":
                print("The available buckets:")
                service_class.list_of_buckets()
                bucket_name = input("Select bucket name: ")
                file_path = input("Enter file path: ")
                service_class.upload_file(file_path,bucket_name)
            else:
                service_class.list_of_buckets()

        else:
            service_class = Route53Service()
            if action_choice == "1":
                zone_name = input("Enter Zone name: ")
                service_class.create_zone(zone_name)
            elif action_choice == "5":
                print(service_class.list_hosted_zone_by_tags())
            elif action_choice == "6":
                zone_id = input("Enter Zone ID: ")
                service_class.list_resource_records(zone_id)
            else:
                zone_id = input("Enter Zone ID: ")
                record_name = input("Enter record name (end with the hosted zone name!): ")
                value = input("Enter value: ")
                ttl = int(input("Enter TTL(seconds): "))
                action_map = {
                    "2": "create",
                    "3": "update",
                    "4": "delete"
                }
                create_or_update_record(service_class, action_map.get(action_choice), zone_id, record_name, value, ttl)


# activate the main function
main()