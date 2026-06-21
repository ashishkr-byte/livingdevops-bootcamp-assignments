
import requests
import os

domain = "https://api.github.com"

username = ""

repo_endpoint = f"{domain}/users/{username}/repos"



def list_repos(endpoint):
    response = requests.get(endpoint)
    # print(dir(response))
    print(response.links)
    if response.status_code == 200:
        repos = response.json()
        print(f"Total Repos: {len(repos)}")
        for repo in repos:
            print(repo['name'])
            # print(repo['description'])

    else:
        print(f"Failed to fetch repositories for user {username}. Status code: {response.status_code}")

# list_repos(repo_endpoint)


def list_repos_with_pagination(endpoint):
    response = requests.get(
        endpoint,
        
        params={
            "per_page":4,
            "page":2
        }
    )
    
    repos = response.json()

    print(f"Total Repos: {len(repos)}")
    for repo in repos:
        print(repo['name'])
        # print(repo['description'])

# list_repos_with_pagination(repo_endpoint)


def create_repo(domain_name, token, payload): # this needs authentication
    endpoint = f"{domain_name}/user/repos"
    response = requests.post(endpoint, headers={"Authorization": f"Bearer {token}"}, json=payload)
    print(response.status_code)
    # print(response.json())
    

github_token = os.getenv("GITHUB_TOKEN")

""" headers = {
    "Authorization": f"Bearer {github_token}",          # your identity, Bearer just means "I'm proving my identity with this token"
    "Accept": "application/vnd.github+json",             # You're telling GitHub "send me the response in JSON format", vnd.github+json is GitHub's specific JSON format
    "X-GitHub-Api-Version": "2022-11-28"            # the version of the github API to use
}
 """

payload = {
    "name": "demo-repo",
    "description": "This is a demo repo",
    "private":False
    # "homepage":
    # "is_template":True
}

# the accept and APi version fields are skippable, but authorisation is not

# response = requests.post(repo_endpoint, headers=headers, json={"name": "demo-repo"})

# print(response.status_code)

# create_repo(domain, github_token, payload)

def delete_repo(domain_name, owner_name, repo, token):
    endpoint = f"{domain_name}/repos/{owner_name}/{repo}"
    response = requests.delete(endpoint, headers={"Authorization": f"Bearer {token}"})
    print(response.status_code)
                            



repo_name = "demo-repo"

delete_repo(domain, username, repo_name, github_token)