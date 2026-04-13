

data "aws_route53_zone" "hosted_zone" {
  name         = var.domain_name
  private_zone = false
}



resource "aws_acm_certificate" "cert" {
  domain_name       = "${var.app_name}.${var.domain_name}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}


# 1. ACM Validation Records (CNAMEs)
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.hosted_zone.zone_id
}

# 2. Application Record (Alias to ALB)
resource "aws_route53_record" "app_record" {
  zone_id = data.aws_route53_zone.hosted_zone.zone_id
  name    = "${var.app_name}.${var.domain_name}"
  type    = "A"

  alias {
    name                   = aws_lb.app_alb.dns_name
    zone_id                = aws_lb.app_alb.zone_id
    evaluate_target_health = true
  }
}

# 3. Certificate Validation Resource
resource "aws_acm_certificate_validation" "cert_validation" {
  certificate_arn         = aws_acm_certificate.cert.arn
  # This links to the CNAME records created in the first block
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}