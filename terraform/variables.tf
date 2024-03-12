variable "project_id" {
  description = "The Project id"
  default = "used-car-analysis"
}

variable "name" {
  description = "The name of the instance"
  default = "Ubuntu-Used-Car-Analysis"
}

variable "machine_type" {
  description = "The default machine type"
  default = "e2-standard-2"
}

variable "boot_image" {
  description = "The Oprating system of the instance"
  default = "Ubuntu 20.04"
}

variable "boot_size" {
  description = "The size of the instance"
  type = number
  default = 30
}