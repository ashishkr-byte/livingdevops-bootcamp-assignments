# 📌 Overview

Building on previous Boto3/AWS automation work, this focuses on **generic API interaction skills** that apply to any internal or third-party system (e.g.GitHub). The goal: be able to confidently read API docs and perform Create, Read, Update, and Delete operations against any REST API.

---


## 🧠 Topics Covered

### 1. Why API Skills Matter
- Nearly every company workflow involves interacting with internal systems or third-party tools (e.g., Wordpress) via APIs.
- Platforms like GitHub and AWS expose APIs so external systems and the public can read/write data (e.g., stock prices, weather data).
- An **API Gateway** sits in front of these APIs to handle:
  - **Authentication** — verifying who's calling.
  - **Rate limiting** — capping calls per second/minute/day to prevent abuse.
  - **Budget/cost control** — e.g., usage limits on paid APIs like OpenAI.

### 2. WordPress REST API — Full CRUD Walkthrough

**Base setup:** domain `mipony.in`, using the WordPress REST `posts` endpoint.

| Operation | Method | Notes |
|-----------|--------|-------|
| Read all posts | `GET /wp-json/wp/v2/posts` | Public, no auth required |
| Read a single user | `GET /wp-json/wp/v2/users/<id>` | Returns `200` even without auth — only fields the API *exposes* (e.g. name) are returned; fields like email are never returned if not exposed |
| Create a post | `POST /wp-json/wp/v2/posts` | Requires payload (`title`, `content`, `status`) **and** authentication |
| Update a post (full) | `PUT` | Requires the post's unique ID |
| Update a post (partial) | `PATCH` | e.g., changing only `status` from `draft` → `publish`, requires post ID |
| Delete a post | `DELETE /wp-json/wp/v2/posts/<id>` | Requires auth + post ID |

**Authentication:** WordPress requires **Basic Auth** using a username + a dedicated **Application Password** (different from your normal login password).

```python
import requests, os

auth = (os.getenv("WP_USERNAME"), os.getenv("WP_APP_PASSWORD"))

payload = {
    "title": "My New Post",
    "content": "Post content here",
    "status": "draft"
}

response = requests.post(
    "https://mipony.in/wp-json/wp/v2/posts",
    json=payload,
    auth=auth
)
print(response.status_code)   # 201 = created successfully
```

**Key debugging moments from the session:**
- Calling `POST` without auth → `401 Unauthorized`.
- Calling `PUT`/`PATCH` without the post ID in the URL → `404 Not Found`.
- Once the post ID was correctly included → `200 OK` on update.

### 3. GitHub REST API

**Base endpoint:** `api.github.com`

| Action | Endpoint | Auth Required? |
|--------|----------|-----------------|
| List a user's public repos | `GET api.github.com/users/<username>/repos` | No |
| Create a repo (under authenticated user) | `POST api.github.com/user/repos` | Yes |
| Delete a repo | `DELETE api.github.com/repos/<owner>/<repo_name>` | Yes |

**Important lesson learned:** Creating a repo via `POST api.github.com/users/<username>/repos` repeatedly returned `404`. The correct endpoint is `api.github.com/user/repos` (singular `user`, no username in the path) — the authenticated user is inferred from the token itself.

**Authentication via HTTP headers:**
```python
import requests, os

token = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"token {token}"}

payload = {"name": "my-new-repo", "private": False}

response = requests.post(
    "https://api.github.com/user/repos",
    headers=headers,
    json=payload
)
print(response.status_code)   # 201 = created successfully
```

**Deleting a repo — another debugging lesson:**
- Using the repo's numeric **ID** in the delete endpoint → `404`.
- Using the repo's **name** instead → `204 No Content` (success, no body returned).

```python
response = requests.delete(
    f"https://api.github.com/repos/{owner}/{repo_name}",
    headers=headers
)
print(response.status_code)   # 204 = deleted successfully
```

### 4. Pagination & Query Parameters
- Pulling large datasets (e.g., thousands of repos) in one call risks overwhelming the system and the network.
- APIs solve this with **pagination**, controlled via query parameters in the URL (after `?`):
  ```python
  params = {"per_page": 30, "page": 2}
  response = requests.get(
      f"https://api.github.com/users/{username}/repos",
      params=params
  )
  ```
- Query parameters in general let you customize *how* data is returned (filtering, sorting, limiting) without changing the endpoint itself.

### 5. HTTP Status Codes Seen in Practice
| Code | Meaning | When it showed up |
|------|---------|---------------------|
| `200` | OK | Successful GET / successful full update |
| `201` | Created | Successful POST (new post / new repo) |
| `204` | No Content | Successful DELETE |
| `401` | Unauthorized | POST without authentication |
| `404` | Not Found | Missing post ID, wrong GitHub endpoint, wrong repo identifier |

### 6. Security Best Practice: Environment Variables for Secrets
- Tokens and passwords should **never** be hardcoded in scripts.
- Use Python's `os` module to read secrets from environment variables:
  ```python
  import os
  token = os.getenv("GITHUB_TOKEN")
  ```

## ✅ What's Implemented Here

- [x] Fetch all WordPress posts (`GET`)
- [x] Fetch public WordPress user data (`GET`)
- [x] Create a new WordPress post with Basic Auth (`POST`)
- [x] Fully update a WordPress post by ID (`PUT`)
- [x] Partially update a WordPress post's status (`PATCH`)
- [x] Delete a WordPress post by ID (`DELETE`)
- [x] List a GitHub user's public repositories (`GET`, unauthenticated)
- [x] Implement pagination using `per_page` and `page` query parameters
- [x] Generate and use a GitHub classic access token (via env variable)
- [x] Create a new GitHub repository (`POST /user/repos`)
- [x] Delete a GitHub repository by name (`DELETE`)
- [x] Use this very script/process to create a README in a GitHub repo programmatically

## 🔜 Next Steps (Upcoming Curriculum)

- AWS Lambda functions (next 3 days of sessions)
- Multiple real-world Lambda use cases
- Python automation for database migrations
- Python automation for Kubernetes

## 📚 Key Takeaways

- The same CRUD ↔ HTTP method mapping (`GET`/`POST`/`PUT`/`PATCH`/`DELETE`) applies across *every* REST API — WordPress, GitHub, or otherwise.
- Always check the **status code** first when debugging — `401` means an auth problem, `404` usually means a wrong endpoint or missing identifier, not necessarily "unauthorized."
- Read API documentation carefully — endpoint structures (like GitHub's `/user/repos` vs `/users/<name>/repos`) aren't always intuitive.
- Use the **correct unique identifier** the API expects (e.g., repo *name* vs repo *ID*) — using the wrong one silently produces a `404` even when the resource exists.
- Always store credentials/tokens in environment variables, never directly in code.
- Pagination via query parameters is essential when working with any API that can return large datasets.

---
*Notes compiled from a live session on WordPress & GitHub API automation with Python, organized into project documentation.*
