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

resource "docker_network" "nova" {
  name = "nova"
}
resource "docker_container" "web_1" {
  name    = "vm-web-1"
  image   = "python:3.12-slim"
  command = ["sleep", "infinity"]
  networks_advanced {
    name = docker_network.nova.name
  }
}
resource "docker_container" "web_2" {
  name    = "vm-web-2"
  image   = "python:3.12-slim"
  command = ["sleep", "infinity"]
  networks_advanced {
    name = docker_network.nova.name
  }
}
