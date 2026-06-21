

import requests

from requests.auth import HTTPBasicAuth

domain = "https://mansipandey.in"

post_endpoint = "/wp-json/wp/v2/posts"

user_endpoint = "/wp-json/wp/v2/users"

app_post_url = domain + post_endpoint

app_user_url = domain + user_endpoint



# response = requests.get(app_post_url)
# print(response.json())

# print(dir(response))
# print(type(response.text)) #--> this is str



# posts = response.json()
# print(len(posts)) -> shows the no of blogs posted on the website

# print(response.json()) #--> this is list


""" def get_post_data (app_post_url):
    response = requests.get(app_post_url).json()
    post_data = []
    for post in response:
        post_data.append({
            "id": post.get("id"),
            "title": post.get("title", {}).get("rendered"),
            "date": post.get("date"),
        })
    print(post_data) """


def get_user_data(app_user_url):
    response = requests.get(app_user_url).json()
    # print(response)
    user_data = []
    for user in response:
        user_data.append({
            # "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"), # this will print None because the email data is not there in the API response as it might be private
            # "slug": user.get("slug"),
        })

    print(user_data)


def create_post(app_post_url, auth, payload):
    
    response = requests.post(app_post_url, auth=auth, json=payload)
    
    print(response.status_code) #even if you autheticate, you will have 401 error

    print(response.json()) # if you have not authenticated yourself then you will get a 401 error telling that you are not alowed to created posts.
    # 401 error in api response means unaiuthorized access, you need to authenticate yourself to perform the action.

    # Moreover, even you autheticate urself, as done in passing auth argument to the function, you will still get a 401 error, WHy ? this has to do with password - see the comment in the line 83.


# get_post_data(app_post_url)
# get_user_data(app_user_url)


post1_data = {
        "title": "Post Title",
        "content": "This is the post body content.",
        "status": "publish" # or "draft", "pending", "private"
    }

username = "abc"
password = "your_password_here" # this is not the user password used to login into th sysytem

# Most API calls do not use the user poassword for authetication, instead they use "Application Password" which is generated for the use to authenticate API calls

auth = HTTPBasicAuth(username, password)

create_post(app_post_url, auth, post_data)


def update_post(base_url, auth, post_id, payload):
    update_url = f"{base_url}/{post_id}"
    response = requests.put(update_url, auth=auth, json=payload)
    print(response.status_code)
    print(response.json())



post_id = 54
update_post1 = {
        "title": "Post draft-update post",
        "content": "This is the post body content - updated data",
        "status": "draft" # or "draft", "pending", "private"
    }

# update_post(app_post_url, auth, post_id, update_post1)

def patch_post(base_url, auth, post_id):
    patch_url = f"{base_url}/{post_id}"
    response = requests.patch(patch_url, auth=auth, json={"status": "publish"})
    print(response.status_code)
    print(response.json())

patch_post(app_post_url, auth, post_id)


def delete_post(base_url, auth, post_id):
    delete_url = f"{base_url}/{post_id}"
    response = requests.delete(delete_url, auth=auth)
    print(response.status_code)
    print(response.json())

delete_post(app_post_url, auth, post_id)