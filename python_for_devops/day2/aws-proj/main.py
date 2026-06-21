

# to fetch the sqs queue and kms data

#  there are two ways to use the helper file. We can import the whole file and then call the functions using the file name or we can import the specific functions that we need to use in the main.py file. Importing the whole file means it imports all the libraries/functions in that file, so this would take up lot of space. Instead importing specific library is a best practice for memory optimisation and code readability.

""" import helper

region = "ap-south-1"

print(helper.get_sqs_with_kms_key(region))
 """


# from helper import get_sqs_with_kms_key
import helper

region = "ap-south-1"

# print(get_sqs_with_kms_key(region))
print(helper.get_sqs_with_kms_key(region))