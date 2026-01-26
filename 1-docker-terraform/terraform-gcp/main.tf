terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  # Configuration options
  project     = "rgpeart-datatalks-de-course"
  region      = "us-east4"
}