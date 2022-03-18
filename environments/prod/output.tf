
# Display the service URL
output "service_url" {
  value = google_cloud_run_service.run_service.status[0].url
}

output "trigger_id" {
  description = "The unique identifier for the Cloud Build trigger."
  value       = google_cloudbuild_trigger.react_trigger.trigger_id
}
