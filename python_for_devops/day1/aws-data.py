
# get the aws resources here

# to talk to AWS, boto3 is used
# boto3 is not a built in library in python, it is provided by AWS.
# so we have to install the using pip

# we will do it in a virtual environment

import boto3
import argparse # to take input from the user in the command line, we can use argparse library. It is a built in library in python.
# so this helps parse the command line arguments and options.


s3 = boto3.resource('s3')
# s3 = boto3.resource('s3', region_name='us-east-1')

# Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)

# which region's S3 buckets the above prints -- the region which is specified in .aws\config file, or the region defined in the line 13.

# ec2 = boto3.client('ec2')

# response = ec2.describe_instances() # since the parameters are optional, we can skip them and just call the function without any parameters.

# print(response["Reservations"][0]["Instances"][0]["InstanceId"])
# print(response["Reservations"][0]["Instances"][0]["State"]["Name"])
# print(response["Reservations"][1]["Instances"][0]["State"]["Name"])
""" 
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(f"{instance["Tags"][0]["Value"]}-{instance["State"]["Name"]}")  """



# now we want data in this format - [[instance_id, state], [instance_id, state], [instance_id, state]]


def list_ec2_instances(region):
    ec2=boto3.client('ec2', region_name=region)
    ec2_data = ec2.describe_instances()["Reservations"]
    instances = []
    for items in ec2_data:
        instances.append([items["Instances"][0]["InstanceId"], items["Instances"][0]["State"]["Name"]])
    return instances


# how to pull data of ec2 instances region specific.

print(list_ec2_instances("us-east-1"))

