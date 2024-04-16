

# Iterate over the list of bucket names and create a module instance for each one
resource "null_resource" "create_buckets" {
  count = length(local.bucket_names)

  triggers = {
    bucket_name = local.bucket_names[count.index]
  }

  provisioner "local-exec" {
    command = "terraform apply -auto-approve"
  }
}

# Define the module instances for each bucket
module "s3_buckets" {
  source = "github.com/terraform-aws-modules/terraform-aws-s3-bucket"

  count = length(local.bucket_names)

  create_bucket                = true
  attach_policy                = true
  attach_public_policy         = true

  bucket_prefix                = local.bucket_names[count.index]
  acl                          = "public-read"  # Allow public read access for the website

  block_public_acls            = false
  block_public_policy          = false
  #ignore_public_acls           = false
  #restrict_public_buckets      = false

  website = {
    index_document = "index.html"
    error_document = "error.html"
  }
  cors_rule = [
    {
      allowed_headers = ["*"]
      allowed_methods = ["GET", "PUT"]
      allowed_origins = ["*"]
      expose_headers  = ["ETag"]
      max_age_seconds = 3600
    }
  ]
  versioning = {
    enabled = true
  }
}
