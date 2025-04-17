resource "aws_s3_bucket" "milvus_object" {
  bucket = "${var.env}-milvus-object"
}

# Get exist ALB was created by Milvus Cluster

data "aws_lb" "milvus_lb" {
  arn = "arn:aws:elasticloadbalancing:ap-southeast-1:{AWS_ACCOUNT_ID}:loadbalancer/net/milvus-service/{id}"
}

data "aws_lb" "milvus_attu" {
  arn = "arn:aws:elasticloadbalancing:ap-southeast-1:{AWS_ACCOUNT_ID}:loadbalancer/app/k8s-attu-94c19f0090/{id}"
}

# Create domain with ACM from AWS
locals {
  milvus_attu_site = "..."
  milvus_endpoint  = "..."
}

resource "aws_route53_record" "milvus_attu" {
  zone_id = "{zone_id}"
  name    = "{name}"
  type    = "CNAME"
  ttl     = "300"
  records = [data.aws_lb.milvus_attu.dns_name]
}

resource "aws_route53_record" "milvus_endpoint" {
  zone_id = "{zone_id}"
  name    = "{name}"
  type    = "CNAME"
  ttl     = "300"
  records = [data.aws_lb.milvus_lb.dns_name]
}
