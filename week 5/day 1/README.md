
<!-- Pushing a custome image into a private repository created in ECR -->

201760452324.dkr.ecr.ap-south-1.amazonaws.com/jan26-week5

format of a ECR repo ARN

<act_id>.dkr.ecr.<aws_region>.amazonaws.com/<repo_name>[:tag]


Steps to push in this repo:

<!--  Tag your image with the ECR repository URI.
The image must be tagged with the full ECR repository URI format -->

docker tag <your image name> <ECR repo URI>:1.0


<!-- Authenticate Docker client with ECR registry using the AWS CLI -->

aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 201760452324.dkr.ecr.ap-south-1.amazonaws.com
