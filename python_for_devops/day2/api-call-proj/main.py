
import requests

post_url = "https://mansipandey.in/wp-json/wp/v2/posts"

# response = requests.get(post_url)


# print(dir(response))
# print(type(response.text)) #--> this is str



posts = response.json()
# print(len(posts)) -> shows the no of blogs posted on the website

print(response.json()) #--> this is list


def get_post_data (post_url):
    response = requests.get(post_url).json()
    post_data = []
    for post in response:
        post_data.append({
            "id": post.get("id"),
            "title": post.get("title", {}).get("rendered"),
            "date": post.get("date"),
        })
    return post_data