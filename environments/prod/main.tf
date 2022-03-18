
terraform {
  required_version = ">= 0.14"

  required_providers {
    # Cloud Run support was added on 3.3.0
    google = ">= 3.3"
  }
}

# Configure GPC
provider "google" {
  project = var.project
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE A CLOUD BUILD TRIGGER
# ---------------------------------------------------------------------------------------------------------------------

resource "google_cloudbuild_trigger" "react_trigger" {

  //Source section
  github {
    owner = "jonaylor89"
    name  = "cyberpunk"

    //Events section
    push {
       branch = "^main$"
    }
  }

  //Configuration section
 filename = "cloudbuild.yaml"
}

# ---------------------------------------------------------------------------------------------------------------------
# DEPLOY A CLOUD RUN SERVICE
# ---------------------------------------------------------------------------------------------------------------------

# Enable Cloud Run
resource "google_project_service" "run_api" {
  service = "run.googleapis.com"

  disable_on_destroy = true
}

# ---------------------------------------------------------------------------------------------------------------------
# EXPOSE THE SERVICE PUBLICLY
# We give all users the ability to invoke the service.
# ---------------------------------------------------------------------------------------------------------------------

# Create the Cloud Run service
resource "google_cloud_run_service" "run_service" {
  name = var.service_name
  location = var.location

  template {
    spec {
      containers {
        image = local.image_name

        env {
          name  = "GCP_TRACING"
          value = "1"
        }

        env {
          name  = "AUDIO_PATH"
          value = "audius"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  # Waits for the Cloud Run API to be enabled
  depends_on = [google_project_service.run_api]
}

# Allow unauthenticated users to invoke the service
resource "google_cloud_run_service_iam_member" "run_all_users" {
  service  = google_cloud_run_service.run_service.name
  location = google_cloud_run_service.run_service.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ---------------------------------------------------------------------------------------------------------------------
# PREPARE LOCALS
# ---------------------------------------------------------------------------------------------------------------------

locals {
  image_name = var.image_name == "" ? "${var.gcr_region}.gcr.io/${var.project}/${var.service_name}:${var.digest}" : var.image_name
}


