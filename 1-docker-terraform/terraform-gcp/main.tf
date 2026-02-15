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

resource "google_storage_bucket" "demo-bucket" {
  name          = "rgpeart-datatalks-de-course-terra-bucket"
  location      = "US"
  force_destroy = true

  # Lifecycle rule to automatically delete objects after 1 day if they are not fully uploaded (incomplete multipart uploads)
  lifecycle_rule {
    condition {
      # Days since the object was created
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}