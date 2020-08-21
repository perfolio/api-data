provider "docker" {}

resource "docker_network" "global" {
  name = "global"
}

resource "docker_image" "factor" {
  name          = "perfolio/factor:latest"
  pull_triggers = ["perfolio/factor:latest.sha256_digest"]
}

##########################
#         Services
###########################

resource "docker_container" "factor" {
  name    = "factor"
  image   = docker_image.factor.latest
  restart = "always"

#   command = ["/code/api/manage.py runserver"]
#   env     = ["SERVICE_ADDRESS=0.0.0.0:52000"]
  ports {
    internal = 8000
    external = 8000
  }
  
  networks_advanced {
    name = docker_network.global.name
  }
}
