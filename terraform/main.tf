# Root Terraform to provision Cloud Run service & secrets for the generated app
# Usage:
#   terraform init
#   terraform apply -var="project_id=YOUR_ID" -var="region=us-central1" -var="service_name=demo_app" -var="image=gcr.io/YOUR_ID/demo_app"

terraform {
  required_version = ">= 1.6.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" { type = string }
variable "region" { type = string, default = "us-central1" }
variable "service_name" { type = string, default = "demo_app" }
variable "image" { type = string }

# Optional: create secrets (values should be set via Secret Manager UI/CLI after creation)
resource "google_secret_manager_secret" "stripe_key" {
  secret_id = "stripe-secret-key"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "stripe_webhook" {
  secret_id = "stripe-webhook-secret"
  replication { automatic = true }
}

resource "google_cloud_run_v2_service" "app" {
  name     = var.service_name
  location = var.region
  template {
    containers {
      image = var.image
      env {
        name  = "STRIPE_SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.stripe_key.name
            version = "latest"
          }
        }
      }
      env {
        name  = "STRIPE_WEBHOOK_SECRET"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.stripe_webhook.name
            version = "latest"
          }
        }
      }
      ports { container_port = 8080 }
    }
  }
  ingress = "INGRESS_TRAFFIC_ALL"
}

resource "google_cloud_run_service_iam_member" "invoker" {
  location = google_cloud_run_v2_service.app.location
  service  = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "service_url" {
  value = google_cloud_run_v2_service.app.uri
}
