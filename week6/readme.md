# Terraform & AWS Infrastructure Bootcamp

This repository contains my personal learning journey, experiments, and code samples related to **Terraform and AWS Infrastructure as Code (IaC)**. 

The goal of this project is to master the fundamentals of cloud infrastructure, focusing on networking, dependency management, and safe state handling.

---
## 🛠 project documentation
open the docx file 2 tier app ecs_using terraform.docx file, which contain screenshots of varios resources which were created by the terraform.


---
## 🛠 Key Concepts Learned

### 1. Resource Management
* **Arguments vs. Attributes:** Learned how to distinguish between **inputs** (arguments used to configure resources) and **outputs** (attributes returned by the cloud provider after creation).
* **Implicit vs. Explicit Dependencies:** * Terraform naturally handles **implicit dependencies** (e.g., a subnet needing a VPC ID).
    * Used `depends_on` for **explicit dependencies** (e.g., ensuring an Internet Gateway is attached before a NAT Gateway is created).

### 2. State & Backend Management
* **Source of Truth:** Understood that the `terraform.tfstate` file is the map between code and cloud resources.
* **Remote Backends:** Migrated from local state files to **AWS S3** for remote storage, enabling team collaboration and better security.
* **Safety Features:** * Enabled **S3 Versioning** to prevent accidental state corruption.
    * Learned the importance of **State Locking** (using DynamoDB) to prevent concurrent operations.

### 3. AWS Networking Architecture
* **Subnets:** Configured Public and Private subnets using `map_public_ip_on_launch`.
* **NAT Gateways:** Managed NAT Gateway deployment, including the requirement for Elastic IPs (EIP) and proper route table associations.
* **The "Route Table" Gotcha:** Learned that defining routes inline within a route table block can lead to configuration drift. Best practice is to use standalone `aws_route` resources for explicit control.

---

## 🚀 Terraform Workflow
This project follows these essential CLI practices:

* `terraform fmt`: Maintains code readability and style.
* `terraform validate`: Ensures configuration syntax is correct.
* `terraform plan`: Previews changes before execution to prevent accidental infrastructure destruction.
* `terraform state list`: Inspects the current state without opening the JSON file.
* `terraform apply -target="..."`: Performs targeted operations on specific resources.

---

## 📝 Best Practices Implemented
* Utilized `variables.tf` to avoid hardcoding values.
* **Infrastructure Tagging:** Used `default_tags` within the `provider "aws"` block to automatically tag all resources for easier tracking of IaC-managed components.
* **Safety:** Always run `terraform plan` before `apply` to avoid unexpected recreation of resources (especially when changing Availability Zones).

---

## 📂 Project Structure
```text
.
├── main.tf           # Main infrastructure resources
├── variables.tf      # Reusable variables
├── providers.tf      # AWS provider configuration
