import json
import requests
import os
import boto3

domain = "https://api.github.com"
username = ""

def get_secret(secretkey):
    response = boto3.client('secretsmanager')
    secret = response.get_secret_value(SecretId=secretkey)['SecretString'] 
    secret_value = json.loads(secret)
    return secret_value["GITHUB_Token"]
    

def create_repo(domain_name, token, payload): # this needs authentication
    endpoint = f"{domain_name}/user/repos"
    response = requests.post(endpoint, headers={"Authorization": f"Bearer {token}"}, json=payload)
    return response.status_code
    
def lambda_handler(event, context):
    # TODO implement
    payload = {
    "name": "demorepo1",
    "description": "This is a demo repo",
    "private":False
    }

    secret_key = os.getenv("access_key")
    github_token = get_secret(secret_key)

    return {
        'statusCode': create_repo(domain, github_token, payload)
        # 'body': json.dumps('Hello from Lambda!')
    }