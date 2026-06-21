# 📌 Overview

- Query AWS services (Secrets Manager, SQS, EC2) across multiple regions
- Process and shape API responses safely
- Be organized into a reusable function library
- Make external (non-AWS) API calls for CRUD-style operations

## 📁 Project Structure

```
(main project folder)/
│
├── venv/                  # Virtual environment (not committed)
├── main.py                # Entry point — imports and calls functions from helper.py
├── helper.py               # Reusable library of utility functions (AWS + API)
└── README.md
```

**Why this structure?**
Separating logic into `main.py` and `helper.py` keeps the main script clean and lets you import *only* the functions you need,just like using built-in methods on Python lists or dictionaries instead of loading everything into memory at once.

## ⚙️ Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # On Windows: 
   ```

2. Install dependencies:
   ```bash
   pip install boto3 requests
   ```

3. Configure AWS credentials (via `aws configure`) before running any Boto3-based functions.

## 🧠 Topics Covered

### 1. AWS Secrets Manager — Listing Secrets
- Used Boto3's `list_secrets` API to fetch all secrets in a given region.
- Parsed the JSON response to pull out each secret's:
  - Name
  - ARN
  - Last accessed date
  - Creation date
- Last-accessed date is useful for identifying **unused/stale secrets**.
- Converted raw datetime strings into a human-readable **"X days ago"** format using a helper function and f-strings.

### 2. Safe Data Access with `.get()`
- Used `dict.get(key, default)` instead of direct key access (`dict[key]`) to avoid runtime errors when a key is missing.
- Rule of thumb: if a key is expected to return a list, default to an **empty list** (`[]`) rather than `None`, so the rest of the code (loops, etc.) doesn't break.

### 3. Amazon SQS — Queues & Compliance Checks
- **Why queues matter:** Systems like SQS, Kafka, and RabbitMQ act as buffers that absorb high volumes of requests (e.g., millions of events/hour) so a downstream database isn't overwhelmed and doesn't crash. The queue holds requests and lets the database consume them at a sustainable pace.
- I Built functions to:
  - `list_sqs_queues()` — list all queue URLs in a region.
  - `get_sqs_attributes()` — fetch attributes for a specific queue.
- **Real-world use case:** Checking whether each queue is encrypted with a **customer-managed KMS key** (`KmsMasterKeyId`) rather than the AWS-default key — a common compliance/security audit requirement.

### 4. Writing Cleaner Python: List Comprehension & Tuples
- Replaced the traditional pattern:
  ```python
  results = []
  for item in data:
      results.append((item['name'], item['value']))
  ```
  with a single-line **list comprehension**:
  ```python
  results = [(item['name'], item['value']) for item in data]
  ```
- List comprehension also supports conditional logic (`if` filters) inline.
- Used **tuples** instead of lists for intermediate row data since tuples are immutable — a good fit for fixed records like `(name, value)` pairs that shouldn't be modified after creation.

### 5. Building a Reusable Helper Library
- Moved all working functions into `helper.py` to create a small internal "library."
- Two ways to import functions, and when to use which:
  ```python
  # Imports everything — loads all functions into memory even if unused
  import helper

  # Imports only what you need —> efficient and standard practice professionally
  from helper import get_sqs_with_kms_key
  ```
- Another best practice -> initialize the Boto3 session/client **once** and pass it into each function, rather than creating a new client per function call, to reduce overhead and API calls.

### 6. API Fundamentals
All AWS services (SQS, EC2, RDS, S3, etc.) are themselves built on APIs. Understanding raw API mechanics is foundational to working with *any* API-based tool or service.

**HTTP Response Code Ranges:**
- pls refer the documentation.docx file in the python_for_devops directory.

**CRUD ↔ HTTP Methods:**
| Operation | HTTP Method |
|-----------|-------------|
| Create | `POST` |
| Read   | `GET` |
| Update | `PATCH` / `PUT` |
| Delete | `DELETE` |

### 7. Making External API Calls with `requests`
- Installed the library: `pip install requests`
- Demonstrated calling a public WordPress REST API endpoint:
  ```python
  import requests

  response = requests.get("https://example.com/wp-json/wp/v2/posts")

  print(response.status_code)   # HTTP status code
  print(response.text)          # Raw response body as a string
  data = response.json()        # Parsed into a Python list/dict
  ```
- Accessed individual posts by index and extracted specific fields (`title`, `date`, `content`) using `.get()` on each post dictionary.
- Looped through all returned posts to extract and print specific fields cleanly.


## 📚 Key Takeaways

- Always default missing dictionary keys with `.get()` to write robust, failure-resistant code.
- Explicitly set the AWS region in every Boto3 client, don't rely on defaults.
- Queues exist to protect downstream systems (like databases) from being overwhelmed by bursts of traffic.
- List comprehensions and tuples lead to more concise, readable, and intention-revealing code.
- A solid understanding of HTTP status codes and CRUD-to-HTTP-method mapping is foundational for working with *any* API, AWS or otherwise.
