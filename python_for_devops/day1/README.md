# Python for DevOps
### Topic: AWS Resource Automation with Python & Boto3

## 1. Why Python for DevOps

- Python is a **critical skill** for senior DevOps and Platform Engineering roles.
- Primarily used for **automation** and building **internal tools/dashboards**.
- It is the **most commonly requested language** in DevOps interviews.

---

## 2. Python Fundamentals Recap

### Lists

Lists are Python's equivalent of arrays. Indexing starts at `0`. Index `-1` always returns the last item.

```python
fruits = ["apple", "banana", "cherry"]

print(fruits[0])   # apple
print(fruits[-1])  # cherry

# Iterating through a list
for fruit in fruits:
    print(fruit)
```

---

### F-Strings

F-strings are the simplest way to embed variables inside strings. Prefix the string with `f` and wrap variables in `{}`.

```python
name = "Ashish"
role = "Devops Professional"

print(f"Hello, {name.capitalize()}! You are a {role}.")
# Output: Hello, Ashish! You are a devops engineer.
```

---

### List Methods — `append()` and `extend()`

| Method | What it does |
|---|---|
| `.append(item)` | Adds a **single item** to the end of the list |
| `.extend(another_list)` | **Merges** another list's items into the existing list |

```python
data = ["i-001", "running"]

all_data = []
all_data.append(data)   # Result: [["i-001", "running"]]  ← nested list

all_data = []
all_data.extend(data)   # Result: ["i-001", "running"]    ← flat merge
```

---

### String Splitting

The `.split(delimiter)` method breaks a string into a list using a specified character as the split point.

```python
regions_input = "ap-south-1 us-east-1 eu-west-1"
regions_list = regions_input.split(" ")

print(regions_list)
# Output: ['ap-south-1', 'us-east-1', 'eu-west-1']
```

Common use in DevOps: extracting passwords, DB names, or config values from a larger string.

---

### Dictionaries

Dictionaries store data as **key-value pairs**.

```python
instance = {"id": "i-001", "state": "running", "region": "ap-south-1"}

print(instance.keys())    # dict_keys(['id', 'state', 'region'])
print(instance.values())  # dict_values(['i-001', 'running', 'ap-south-1'])

```

---

## 3. Environment Setup

Always use a **virtual environment** to avoid unnecessarily installing large libraries in your global Python installation context. Instead use virtual environment to install the required libraries as per project requirements. Moreover, installing packages with `pip` globally is discouraged. A virtual environment isolates dependencies to the project, preventing version conflicts.

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
\venv\Scripts\Activate.ps1 -> Windows powershell
#venv\Scripts\activate.bat  ->  Windows CMD

# Install Boto3 inside the virtual environment
pip install boto3

# Verify installation
pip freeze
```

---

## 4. AWS + Boto3 Integration

### Authentication & Authorization

Two concepts to understand before making AWS API calls:

| Term | Meaning |
|---|---|
| **Authentication** | Proving who you are (credentials / login) |
| **Authorization** | Having permission to access a specific resource. This means to ensure your IAM user/role has the correct permissions |

One more thing to note is AWS communicates via **JSON** (key-value pairs). This will become much handy later when reading API response and extracting required parameters from that.


Configure credentials via:
```bash
aws configure
# Enter: AWS Access Key ID, Secret Access Key, Region, Output format
```

---

### Creating a Boto3 Client

```python
import boto3

# Create a client for a specific AWS service
s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2')

# With explicit region
ec2_client = boto3.client('ec2', region_name='us-east-1')
```
> If you don't explicitly define a region, boto3 considers the default region as the one which was given during `aws configure` command. 
---

### Listing S3 Buckets

```python
import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    print(bucket['Name'])
```

---

### Listing EC2 Instances

```python
import boto3

ec2 = boto3.client('ec2', region_name='ap-south-1')
response = ec2.describe_instances()

print(response) 
```

> **Troubleshooting tip:** If you get an `AuthorizationFailure` error, your IAM user likely does not have the permission to access that AWS resource.

---

## 5. Parsing JSON Responses

The raw JSON from AWS API calls can look messy. Use a JSON formatter tool (online or in your IDE) to visualize the structure.

### JSON Structure Concepts

```
Response (parent)
└── Reservations (list)
    └── [0] (first reservation — child)
        └── Instances (list)
            └── [0] (first instance)
                ├── InstanceId   ← sibling
                └── State        ← sibling
                    └── Name     ← child of State
```

- **Parent → Child**: Navigate inward
- **Siblings**: Same level, accessed directly

### Extracting Instance ID and State

```python
import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances()

# Loop through reservations and instances
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        print(f"ID: {instance_id} | State: {state}")
```

---

## 6. Building a Reusable Function

Encapsulate the EC2 logic in a function. A function is created to do **one specific task**.

The output format is a **list of lists**: `[[InstanceId, State], [InstanceId, State], ...]`  
This structure is easy to write to Excel later.

```python
import boto3

def list_ec2_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()

    instance_data = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instance_data.append([instance_id, state])

    return instance_data


# Call the function
data = list_ec2_instances('ap-south-1')
print(data)
# Output: [['i-0abc123', 'running'], ['i-0xyz456', 'terminated']]
```

---

## 7. Multi-Region Support with argparse

Instead of hardcoding the region, accept it as a **command-line argument** using the `argparse` library.

```python
import boto3
import argparse


def list_ec2_instances(region):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_instances()

    instance_data = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instance_data.append([instance_id, state])

    return instance_data


# Set up argument parser
parser = argparse.ArgumentParser() # initializing the parser
parser.add_argument('--region', nargs='+', type =str, help="AWS regions")
args = parser.parse_args()

# if type=list, this is problem because argparse applies type to each individual argument value, not the whole list. So list("us-east-1") means ['u', 's', '-', 'e', 'a', 's', 't', '-', '1'], so better is type=str

# nargs stands for "number of arguments.tells the command-line parser how many command-line arguments should be consumed by a single option.

# nargs allows to accept zero, multiple, or a variable number of arguments, which it then automatically bundles into a Python list.

```

**Running the script from terminal:**

```bash
# Single region
python3 script.py --region ap-south-1

# Multiple regions (space-separated)
python3 script.py --region ap-south-1 us-east-1 eu-west-1
```
---
