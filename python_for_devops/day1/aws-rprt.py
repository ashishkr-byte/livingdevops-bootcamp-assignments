

import boto3
import argparse
# argparse module - used to take input from the user in the command line. It is a built in library in python.
# so this helps parse the command line arguments.


parser = argparse.ArgumentParser() # initializing the parser

parser.add_argument("--region", nargs="+", type=str, help="AWS region") 

# if type=list, this is problem because argparse applies type to each individual argument value, not the whole list. So list("us-east-1") means ['u', 's', '-', 'e', 'a', 's', 't', '-', '1'], so better is type=str

# nargs stands for "number of arguments.tells the command-line parser how many command-line arguments should be consumed by a single option.

# nargs allows to accept zero, multiple, or a variable number of arguments, which it then automatically bundles into a Python list.





# parser.add_argument("--services",type=list, help="aWS services") 





# tell it to use argument called region.
# type = str - means taking one region as input, If I want it to work for multiple regions, I habve to use list as the type



def list_ec2_instances(region):
    ec2=boto3.client('ec2', region_name=region)
    ec2_data = ec2.describe_instances()["Reservations"]
    instances = []
    for items in ec2_data:
        instances.append([region, items["Instances"][0]["InstanceId"], items["Instances"][0]["State"]["Name"]])
    return instances


args = parser.parse_args() # this will parse the command line arguments and store them in the args variable.

# print(list_ec2_instances(args.region))

""" if len(args.region) > 0:
    for region in args.region:
        print(f"EC2 instances in {region} region:")
        print(list_ec2_instances(region))
else:
    print("Please provide at least one region using --region argument.") """

""" try: 
    for region in args.region:
        print(f"EC2 instances in {region} region:")
        print(list_ec2_instances(region))
except Exception as e:
    print("Either no regions is provided or the provided region is invalid")
 """


def accumulate_ec2_data ():
    if len(args.region) > 0:
        all_ec2_data = []
        for region in args.region:
            all_ec2_data.extend(list_ec2_instances(region))
        return all_ec2_data

    else:
        return "provide region using --region argument."

print(accumulate_ec2_data())
