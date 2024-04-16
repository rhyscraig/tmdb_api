terraform {

  backend "s3" {
    bucket = "terraform-tfstate-bucket-395101865577"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }

}

provider "aws" {
  region = "eu-west-2"
}