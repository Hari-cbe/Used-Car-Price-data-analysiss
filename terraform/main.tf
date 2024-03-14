locals{
    project_id = var.project_id
}

provider "google" {
    project = local.project_id
    credentials = var.service_acc
    region  = "us-central1"
    zone    = "us-central1-b"
}

resource "google_project_service" "compute_service" {
    project = local.project_id
    service = "compute.googleapis.com"
  
}

resource "google_compute_instance" "vm_instance" {
    name = var.name
    machine_type = var.machine_type

    tags=["ubuntu-tunstance-car"]

    boot_disk {
      initialize_params {
            image = var.boot_image
            size = var.boot_size
        }
    }

    metadata_startup_script = "sudo apt-get update; sudo apt-get install -yq build-essential python-pip rsync; pip install flask"

    network_interface {
      network = "default"
    access_config {
     // Include this section to give the VM an external ip address
    }
  }

}