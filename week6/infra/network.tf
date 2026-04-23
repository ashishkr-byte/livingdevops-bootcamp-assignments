
# VPC

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = var.vpc_name
  }
}


# 2 public subnets

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = var.primary_az
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public1"
  }
}

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = var.secondary_az
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.vpc_name}-public2"
  }
}



# 1 route table for public subnets and add a route to IGW in public route table

resource "aws_route_table" "public_RT" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "${var.vpc_name}-public_RT"
  }
}


# Internet Gateways

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.vpc_name}-IGW"
  }
}


# VPC id already mentioned in aws_internet_gateway above so no need to mention the

# resource "aws_internet_gateway_attachment" "gw_attach" {
#   internet_gateway_id = aws_internet_gateway.gw.id
#   vpc_id              = aws_vpc.main.id
# }





# Add public subnets to the route table

resource "aws_route_table_association" "a" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public_RT.id

}

resource "aws_route_table_association" "b" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public_RT.id
}

# the above code is repeated two times, there is a better way to do it, which we will learn later.







# Nat gw (only one for cost saving)

resource "aws_nat_gateway" "natgw" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public1.id

  tags = {
    Name = "gw NAT"
  }

  # depends on -- uses list item [item1,item2,item3..........]
  # so in depends on we can create multiple dependencies
  # in implicit dependecies -- format is resource.name.id -- because we need the id
  # in explicit depen -- we dont need the data , we just make sure that resource is present so the format is [resource.name]

  depends_on = [aws_internet_gateway.gw]

}



# attach elastic IP to NAt GW

resource "aws_eip" "nat" {
}



# 2 private subnets

resource "aws_subnet" "private1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.3.0/24"
  availability_zone       = var.primary_az
  map_public_ip_on_launch = false # although the default value is false


  tags = {
    Name = "${var.vpc_name}-private1"
  }
}

resource "aws_subnet" "private2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.4.0/24"
  availability_zone       = var.secondary_az
  map_public_ip_on_launch = false # although the default value is false

  tags = {
    Name = "${var.vpc_name}-private2"
  }
}



# 1 route table for private subnets and add a route to NAT GW in route table

resource "aws_route_table" "private_RT" {
  vpc_id = aws_vpc.main.id

  /* route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.natgw.id
  } */

  tags = {
    Name = "${var.vpc_name}-private_RT"
  }
}

resource "aws_route" "r" {
  route_table_id         = aws_route_table.private_RT.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.natgw.id
}


# Add private subnet to route table

resource "aws_route_table_association" "c" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private_RT.id

}

resource "aws_route_table_association" "d" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private_RT.id
}



# RDS subnet


resource "aws_subnet" "rds_subnet1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.5.0/24"
  availability_zone       = var.primary_az
  map_public_ip_on_launch = false # although the default value is false


  tags = {
    Name = "${var.vpc_name}-rds1"
  }
}

resource "aws_subnet" "rds_subnet2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.6.0/24"
  availability_zone       = var.secondary_az
  map_public_ip_on_launch = false # although the default value is false

  tags = {
    Name = "${var.vpc_name}-rds2"
  }
}