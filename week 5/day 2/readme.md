
<!-- for database -->

user: postgres
password: Admin1234
db name: portfolio_website
port 5432
host: endpoint of RDS instance

<!-- format of a RDS instance endpoint
<instance_name>.<unique identifier>.<region>.rds.amazonaws.com -->

<!-- unique identifier -- unique to every AWS account -->

<!-- DB_LINK = "postgresql://{username}:{password}@{host}:5432/{database_name}" -->

DB_LINK = "postgresql://postgres:password@portfolio-website.cnw24ci2ap8b.ap-south-1.rds.amazonaws.com:5432/portfolio_website"






