terraform {
  required_version = ">= 1.0"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "pedidos_veloz" {
  metadata {
    name = "pedidos-veloz"
  }
}

resource "kubernetes_config_map" "pedidos_config" {
  metadata {
    name = "pedidos-config"
    namespace = kubernetes_namespace.pedidos_veloz.metadata[0].name
  }

  data = {
    DB_HOST = "postgres"
    DB_NAME = "pedidosdb"
    DB_USER = "postgres"
  }
}

resource "kubernetes_secret" "pedidos_secret" {
  metadata {
    name = "pedidos-secret"
    namespace = kubernetes_namespace.pedidos_veloz.metadata[0].name
  }

  data = {
    DB_PASSWORD = base64encode("postgres")
  }

  type = "Opaque"
}
