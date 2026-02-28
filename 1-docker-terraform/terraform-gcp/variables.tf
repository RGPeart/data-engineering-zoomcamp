variable "credentials_path" {
    description = "My Credentials"      # Description of the variable
    default = "./keys/my-creds.json"    # Relative path to the service account key file containing the credentials for authenticating with Google Cloud
}

variable "project" {
    description = "Project Name"            # Description of the variable
    default = "rgpeart-datatalks-de-course" # The Google Cloud project where the resources will be created
}

variable "region" {
    description = "Project Region"  # Description of the variable
    default = "us-east4"            # The region where the resources will be created (e.g., us-east4, us-west1, europe-west1)
}

variable "location" {
    description = "Project Location"    # Description of the variable
    default = "US"                      # The location where the resources will be created (e.g., US, EU, ASIA)
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"    # Description of the variable
    default = "demo_dataset"                    # The name of the BigQuery dataset to be created
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"                  # Description of the variable
    default = "rgpeart-datatalks-de-course-terra-bucket"    # The name of the Google Cloud Storage bucket to be created
}

variable "gcs_storage_class" {
    description = "Bucket Storage Class"    # Description of the variable
    default = "STANDARD"                    # The storage class for the Google Cloud Storage bucket
}