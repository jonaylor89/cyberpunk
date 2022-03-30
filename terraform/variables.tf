# ---------------------------------------------------------------------------------------------------------------------
# REQUIRED PARAMETERS
# These variables are expected to be passed in by the operator.
# ---------------------------------------------------------------------------------------------------------------------

variable "project" {
  description = "The project ID where all resources will be launched."
  type        = string
}

variable "location" {
  description = "The location (region or zone) to deploy the Cloud Run services. Note: Be sure to pick a region that supports Cloud Run."
  type        = string
}

variable "gcr_region" {
  description = "Name of the GCP region where the GCR registry is located. e.g: 'us' or 'eu'."
  type        = string
}

variable "service_name" {
  description = "The name of the Cloud Run service to deploy."
  type        = string
  default     = "cyberpunk"
}


variable "image_name" {
  description = "The name of the image to deploy. Defaults to a publicly available image."
  type        = string
  default     = "us.gcr.io/cyberpunk-341504/cyberpunk/cyberpunk:latest"
}

variable "branch_name" {
  description = "Branch name used to trigger builds."
  type        = string
  default     = "main"
}

variable "digest" {
  description = "The docker image digest or tag to deploy."
  type        = string
  default     = "latest"
}