variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  description = "GCP Region (e.g. us-central1)"
}

variable "service_name" {
  type        = string
  description = "Name of the Cloud Run service"
}

variable "image_url" {
  type        = string
  description = "Docker image URL in Artifact Registry"
}

variable "gcp_credentials" {
    type = string
    description = "Credentials of GCP"
    sensitive = true
}

variable cloud_run_sa_email {
    type = string
    description = "cloud run compute engine"
}