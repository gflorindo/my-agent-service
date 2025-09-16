terraform {
  backend "gcs" {
    bucket = "genai-dawright-terraform-state"
    prefix = "my-agent-service/dev"
  }
}
