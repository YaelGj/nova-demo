# Pizzeria Nova : les « VM » sont des conteneurs (fournisseur kreuzwerker/docker).
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "4.6.0"
    }
  }
}

provider "docker" {}

# Image des « VM », construite à partir de vm/Dockerfile : elle sert /srv sur le port 8000.
resource "docker_image" "vm" {
  name = "nova-vm"
  build {
    context = "${path.module}/vm"
  }
}

resource "docker_network" "nova" {
  name = "nova"
}
resource "docker_container" "web_1" {
  name  = "vm-web-1"
  image = docker_image.vm.image_id
  ports {
    internal = 8000
    external = 8081
  }
  networks_advanced {
    name = docker_network.nova.name
  }
}
resource "docker_container" "web_2" {
  name  = "vm-web-2"
  image = docker_image.vm.image_id
  ports {
    internal = 8000
    external = 8082
  }
  networks_advanced {
    name = docker_network.nova.name
  }
}
