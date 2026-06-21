
import boto3
from datetime import datetime

# the various functions here are also called libraries. For each service we have a function so that we can call a library as per our need in the main.py file and accordingly do the job.

def list_ec2_instances(region):
    ec2=boto3.client('ec2', region_name=region)
    ec2_data = ec2.describe_instances()["Reservations"]
    instances = []
    for items in ec2_data:
        instances.append([region, items["Instances"][0]["InstanceId"], items["Instances"][0]["State"]["Name"]])
    return instances


def list_secretmanager_secrets(region):
    secretsmanager = boto3.client('secretsmanager', region_name = region)

    response = secretsmanager.list_secrets()

    

    secret_list_data= response.get("SecretList", [])


    for item in secret_list_data:
        name = item.get("Name")
        creation_date = item.get("CreatedDate")
        
        # Calculate age of the secret
        current_time = datetime.now(creation_date.tzinfo) # to ensure that the current time is in the same timezone as the creation date
        age = current_time - creation_date
        days = age.days

        print(f"Secret: {name}")
        print(f"Created: {creation_date}")
        print(f"This secret is {days} days old") # {hours} hours, {minutes} minutes")
        print("-" * 50) # separator for better readability of output


def list_sqs_queues(region):
    sqs = boto3.client('sqs', region_name = region)
    response = sqs.list_queues()

    return response


def get_queue_attribute(region, queue_url):
    sqs = boto3.client('sqs', region_name = region)
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['KmsMasterKeyId']
    )
    return response.get("Attributes",{}).get("KmsMasterKeyId", "KMS key not found")


def get_sqs_with_kms_key(region):
    
    queue_urls = list_sqs_queues(region).get("QueueUrls", [])
    

    # Using List comprehension to achieve the same result in a more concise way

    queue_with_kms_key = [(url, get_queue_attribute(region, url)) for url in queue_urls]

    return queue_with_kms_key
