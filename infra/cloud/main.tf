# Pizzeria Nova « comme sur un cloud » : l'image de l'API construite par Terraform,
# N instances derrière un répartiteur nginx. Passer de 2 à 3 : variable instances.
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "4.6.0"
    }
  }
}

provider "docker" {}

variable "instances" {
  description = "Nombre d'instances de l'API Nova derrière le répartiteur"
  type        = number
  default     = 2
}

resource "docker_network" "nova_cloud" {
  name = "nova-cloud"
}

# Construit l'image à partir du Dockerfile à la racine du dépôt.
resource "docker_image" "nova" {
  name = "nova:cloud"
  build {
    context = "${path.module}/../.."
  }
}

resource "docker_container" "api" {
  count = var.instances
  name  = "nova-api-${count.index + 1}"
  image = docker_image.nova.image_id
  networks_advanced {
    name = docker_network.nova_cloud.name
  }
}

resource "docker_container" "repartiteur" {
  name  = "nova-repartiteur"
  image = "nginx:1.30.6"
  ports {
    internal = 80
    external = 8080
  }
  # Configuration générée à partir de la liste des instances.
  upload {
    file = "/etc/nginx/conf.d/default.conf"
    content = templatefile("${path.module}/nginx.conf.tftpl", {
      instances = docker_container.api[*].name
    })
  }
  networks_advanced {
    name = docker_network.nova_cloud.name
  }
}

output "adresse" {
  value = "http://localhost:8080/commandes"
}
