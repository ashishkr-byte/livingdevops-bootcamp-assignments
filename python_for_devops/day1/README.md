# Python for DevOps — Session Notes
### Topic: AWS Resource Automation with Python & Boto3
**Class Date:** April 22, 2026 | **Instructor:** Akhilesh Mishra

---

## Overview

This session covered Python fundamentals needed for DevOps work, and then moved into using **Boto3** (the AWS SDK for Python) to interact with AWS services — specifically EC2 and S3. The end goal is to build a script that pulls AWS resource data across multiple regions and exports it to an Excel sheet.

---

## Table of Contents

1. [Why Python for DevOps](#1-why-python-for-devops)
2. [Python Fundamentals Recap](#2-python-fundamentals-recap)
   - [Lists](#lists)
   - [F-Strings](#f-strings)
   - [List Methods — append() and extend()](#list-methods----append-and-extend)
   - [String Splitting](#string-splitting)
   - [Dictionaries](#dictionaries)
3. [Environment Setup](#3-environment-setup)
4. [AWS + Boto3 Integration](#4-aws--boto3-integration)
   - [Creating a Boto3 Client](#creating-a-boto3-client)
   - [Listing S3 Buckets](#listing-s3-buckets)
   - [Listing EC2 Instances](#listing-ec2-instances)
5. [Parsing JSON Responses](#5-parsing-json-responses)
6. [Building a Reusable Function](#6-building-a-reusable-function)
7. [Multi-Region Support with argparse](#7-multi-region-support-with-argparse)
8. [Accumulating Data Across Regions](#8-accumulating-data-across-regions)
9. [Next Steps](#9-next-steps)

---

## 1. Why Python for DevOps

- Python is a **critical skill** for senior DevOps and Platform Engineering roles.
- Primarily used for **automation** and building **internal tools/dashboards**.
- It is the **most commonly requested language** in DevOps interviews.
- Goal for the next 3 weeks: Learn enough Python to build on it confidently.

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
name = "Akhilesh"
role = "devops engineer"

print(f"Hello, {name.capitalize()}! You are a {role}.")
# Output: Hello, Akhilesh! You are a devops engineer.
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

> **Important:** When accumulating AWS data from multiple regions, use `.extend()` to keep the list flat so it can be written cleanly to Excel.

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
instance = {"id": "i-001", "state": "running", "region": "us-east-1"}

print(instance.keys())    # dict_keys(['id', 'state', 'region'])
print(instance.values())  # dict_values(['i-001', 'running', 'us-east-1'])

for key, value in instance.items():
    print(f"{key}: {value}")
```

---

## 3. Environment Setup

Always use a **virtual environment** to avoid polluting your global Python installation.

```bash
# Check Python version
python3 --version

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

# Install Boto3 inside the virtual environment
pip install boto3

# Verify installation
pip list
```

> **Why virtual environments?**  
> Installing packages with `pip` globally is discouraged. A virtual environment isolates dependencies to the project, preventing version conflicts.

---

## 4. AWS + Boto3 Integration

### Authentication & Authorization

Two concepts to understand before making AWS API calls:

| Term | Meaning |
|---|---|
| **Authentication** | Proving who you are (credentials / login) |
| **Authorization** | Having permission to access a specific resource |

AWS communicates via **JSON** (key-value pairs). Ensure your IAM user/role has the correct permissions:
- For S3: `AmazonS3FullAccess` or equivalent
- For EC2: `AmazonEC2FullAccess` or `Admin Access`

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

ec2 = boto3.client('ec2', region_name='us-east-1')
response = ec2.describe_instances()

print(response)  # Raw JSON — use a formatter to read this easily
```

> **Troubleshooting tip:** If you get an `AuthorizationFailure` error, your IAM user likely has S3 access but not EC2. Add `EC2FullAccess` (or `AdminAccess`) to your IAM role/user in the AWS Console.

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

- **Parent → Child**: Navigate inward (drill down)
- **Siblings**: Same level, accessed directly

### Extracting Instance ID and State

```python
import boto3

ec2 = boto3.client('ec2', region_name='us-east-1')
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

Encapsulate the EC2 logic in a function. A function should do **one specific task**.

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
data = list_ec2_instances('us-east-1')
print(data)
# Output: [['i-0abc123', 'running'], ['i-0xyz456', 'terminated']]
```

> **Why `return` instead of `print`?**  
> `print` just displays data. `return` sends the data back to the caller so it can be used, stored, or passed to other functions (like an Excel writer).

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
parser = argparse.ArgumentParser(description="List EC2 instances across regions")
parser.add_argument('--regions', nargs='+', required=True, help="One or more AWS regions")
args = parser.parse_args()
```

**Running the script from terminal:**

```bash
# Single region
python3 script.py --regions us-east-1

# Multiple regions (space-separated)
python3 script.py --regions ap-south-1 us-east-1 eu-west-1
```

> **Key `argparse` concepts:**
> - `nargs='+'` → accepts one or more values as a list
> - `required=True` → argument cannot be omitted
> - `args.regions` → holds the list of regions passed in

---

## 8. Accumulating Data Across Regions

Loop through all provided regions, collect data from each, and merge everything into one flat list using `.extend()`.

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
            instance_data.append([instance_id, state, region])  # include region for filtering in Excel

    return instance_data


# Argument parsing
parser = argparse.ArgumentParser(description="List EC2 instances across regions")
parser.add_argument('--regions', nargs='+', required=True)
args = parser.parse_args()

# Initialize outside conditional to avoid reference errors
all_instance_data = []

if len(args.regions) > 0:
    for region in args.regions:
        region_data = list_ec2_instances(region)
        all_instance_data.extend(region_data)   # extend, NOT append

print(all_instance_data)
# This list is now ready to be passed to an Excel writer function
```

> **`append` vs `extend` — why it matters here:**
> ```python
> # append → creates nested list (wrong for Excel)
> all_data = []
> all_data.append(['i-001', 'running', 'us-east-1'])
> # Result: [['i-001', 'running', 'us-east-1']]  ✓ for one, but...
> all_data.append(['i-002', 'stopped', 'ap-south-1'])
> # Result: [['i-001', ...], ['i-002', ...]]  — nested, harder to flatten
>
> # extend → merges cleanly (correct for multi-region accumulation)
> all_data.extend(['i-001', 'running', 'us-east-1'])
> ```
> Use `extend` when the function already returns a list and you want to merge its items into the parent list.

---

## 9. Next Steps

| Task | Details |
|---|---|
| **Review Recording** | Re-watch the class and follow along with the code steps above |
| **Read Boto3 Docs** | Visit [boto3.amazonaws.com/v1/documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and experiment with examples |
| **Write Excel Function** | Use the `all_instance_data` list and write it to an `.xlsx` file (next class topic) |
| **Project Structure** | Organize the code into a proper Python project with separate modules |
| **Extend to Other Services** | Add `--services` argument to pull data from RDS, S3, Secrets Manager, etc. |
| **Study Python** | Spend time on Python fundamentals over the next 3 weeks |

---

## Quick Reference

```bash
# Virtual environment
python3 -m venv venv && source venv/bin/activate
pip install boto3

# Configure AWS credentials
aws configure

# Run the script
python3 script.py --regions us-east-1 ap-south-1
```

---

> **Instructor's advice:** Don't memorize syntax for third-party libraries — use documentation and AI tools to look up correct syntax when needed. Focus on understanding the *logic and flow* of the code.
