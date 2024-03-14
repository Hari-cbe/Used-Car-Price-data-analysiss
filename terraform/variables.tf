variable "project_id" {
  description = "The Project id"
  default = "used-car-analysis"
}

variable "service_acc" {
  description = "Path to the service account"
  default = "/home/hari/Coding/DataEngineering/Used-Car-Price-data-analysiss/used-car-analysis-sr-key.json"
}

variable "name" {
  description = "The name of the instance"
  default = "ubuntu-used-car-analysis"
}

variable "machine_type" {
  description = "The default machine type"
  default = "e2-standard-2"
}

variable "boot_image" {
  description = "The Oprating system of the instance"
  default = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2004-lts"
}

variable "boot_size" {
  description = "The size of the instance"
  type = number
  default = 30
}