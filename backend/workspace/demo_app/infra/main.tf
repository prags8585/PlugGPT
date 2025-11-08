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

resource "google_secret_manager_secret" "stripe_key" {
  secret_id = "stripe-secret-key"
  replication { automatic = true }
}

resource "google_secret_manager_secret" "stripe_webhook" {
  secret_id = "stripe-webhook-secret"
  replication { automatic = true }
}

# You could also add firebase creds as a secret, but commonly injected via env in CI.

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