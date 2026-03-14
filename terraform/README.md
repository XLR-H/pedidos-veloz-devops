# Terraform – Infraestrutura como Código

Esta pasta demonstra como recursos do Kubernetes podem ser gerenciados utilizando Terraform.

No projeto Pedidos Veloz, o Terraform poderia ser utilizado para:

- criar namespaces
- gerenciar ConfigMaps
- gerenciar Secrets
- provisionar recursos do cluster

Neste exemplo foi criado um protótipo que define:

- namespace da aplicação
- configmap com variáveis de ambiente
- secret com credenciais do banco
