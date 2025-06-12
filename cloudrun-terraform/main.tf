terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_v2_service" "api_cloud_run" {
  name     = var.service_name
  location = var.region

  template {
    service_account = var.cloud_run_sa_email
    containers {
      image = var.image_url
    }
  }

  traffic {
    percent         = 100
  }
}


resource "google_cloud_run_service_iam_member" "invoker" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_v2_service.api_cloud_run.name

  role   = "roles/run.invoker"
  member = "allUsers" # Change to a specific service account if needed
}