# Pedidos Veloz DevOps

Este projeto foi desenvolvido como parte da disciplina de Cloud DevOps e
demonstra a modernização de uma aplicação distribuída utilizando
conceitos de arquitetura de microserviços, conteinerização e
orquestração em ambientes cloud-native.

A proposta do trabalho consiste em construir um MVP funcional que
permita executar a aplicação localmente com Docker Compose e também em
um cluster Kubernetes, simulando um ambiente de produção com práticas
modernas de DevOps.

------------------------------------------------------------------------

## Objetivo do projeto

O objetivo principal é demonstrar como uma aplicação de e-commerce pode
ser organizada em microserviços independentes e implantada utilizando
contêineres Docker e orquestração com Kubernetes.

Durante o desenvolvimento foram aplicados conceitos importantes como
isolamento de serviços, configuração centralizada, gerenciamento de
segredos, verificação de saúde das aplicações e comunicação entre
microserviços.

------------------------------------------------------------------------

## Arquitetura da aplicação

A aplicação representa uma plataforma simplificada de pedidos online
chamada **Pedidos Veloz**.

O sistema foi dividido em quatro microserviços principais.

O serviço **Gateway** funciona como ponto de entrada da aplicação. Todas
as requisições externas passam por ele, que então encaminha as chamadas
para os serviços internos.

O serviço **Pedidos** é responsável por criar e consultar pedidos no
banco de dados.

O serviço **Pagamentos** simula a aprovação de pagamentos para um
pedido.

O serviço **Estoque** simula a reserva de itens solicitados.

Para armazenamento dos pedidos foi utilizado o **PostgreSQL**,
executando em um container separado.

O fluxo principal funciona da seguinte forma: o cliente envia uma
requisição para o gateway, que primeiro solicita a reserva do item no
serviço de estoque, depois cria o pedido no serviço de pedidos e, por
fim, solicita a confirmação do pagamento ao serviço de pagamentos.

------------------------------------------------------------------------

## Estrutura do projeto

O projeto foi organizado de forma que cada microserviço possua seu
próprio diretório e sua própria imagem Docker.

    pedidos-veloz-devops
    │
    ├── services
    │   ├── gateway
    │   ├── pedidos
    │   ├── pagamentos
    │   └── estoque
    │
    ├── docker
    │   └── docker-compose.yml
    │
    ├── k8s
    │   ├── namespace.yaml
    │   ├── configmap.yaml
    │   ├── secret.yaml
    │   ├── postgres-deployment.yaml
    │   ├── postgres-service.yaml
    │   ├── pedidos-deployment.yaml
    │   ├── pagamentos-deployment.yaml
    │   ├── estoque-deployment.yaml
    │   └── gateway-deployment.yaml
    │
    └── README.md

Essa organização facilita a manutenção e permite que cada serviço evolua
de forma independente.

------------------------------------------------------------------------

## Execução local com Docker Compose

O ambiente de desenvolvimento foi padronizado utilizando Docker Compose.
Dessa forma, todos os serviços podem ser iniciados com um único comando.

Para subir a aplicação localmente basta executar o seguinte comando na
raiz do projeto:

    docker compose -f docker/docker-compose.yml up --build

Após a inicialização, o gateway ficará disponível localmente e será
possível realizar chamadas HTTP para a aplicação.

Para verificar se o serviço está funcionando, pode-se executar:

    curl http://localhost:5003/health

Para simular um pedido completo utilizando todos os microserviços,
execute:

    curl -X POST http://localhost:5003/pedido-completo \
    -H "Content-Type: application/json" \
    -d '{"cliente":"Rafael","item":"Notebook","quantidade":1,"valor":3500}'

Esse comando irá acionar o gateway, que por sua vez se comunicará com os
serviços de estoque, pedidos e pagamentos.

------------------------------------------------------------------------

## Execução em Kubernetes

Para simular um ambiente de produção foi utilizado Kubernetes através do
Minikube.

Primeiro é necessário criar os recursos básicos da aplicação no cluster.

    kubectl apply -f k8s/namespace.yaml
    kubectl apply -f k8s/configmap.yaml
    kubectl apply -f k8s/secret.yaml

Em seguida são implantados o banco de dados e os microserviços.

    kubectl apply -f k8s/postgres-deployment.yaml
    kubectl apply -f k8s/postgres-service.yaml
    kubectl apply -f k8s/pedidos-deployment.yaml
    kubectl apply -f k8s/pagamentos-deployment.yaml
    kubectl apply -f k8s/estoque-deployment.yaml
    kubectl apply -f k8s/gateway-deployment.yaml

Como as imagens foram construídas localmente, é necessário carregá-las
para dentro do ambiente do Minikube.

    minikube image load pedidos-service:latest
    minikube image load docker-pagamentos:latest
    minikube image load docker-estoque:latest
    minikube image load docker-gateway:latest

Após isso, é possível obter a URL externa do gateway executando:

    minikube service gateway -n pedidos-veloz --url

Com essa URL será possível acessar o sistema da mesma forma que no
ambiente local.

------------------------------------------------------------------------

## Decisões técnicas adotadas

A linguagem Python com Flask foi escolhida para simplificar a criação
dos microserviços e permitir foco nos conceitos de infraestrutura e
DevOps.

Docker foi utilizado para padronizar o ambiente de execução e garantir
que todos os serviços possam ser executados de forma consistente.

Docker Compose foi utilizado para facilitar o desenvolvimento local,
permitindo subir todos os containers com um único comando.

Kubernetes foi adotado como plataforma de orquestração, permitindo
gerenciar os containers, controlar a disponibilidade dos serviços e
facilitar futuras estratégias de escalabilidade.

ConfigMaps e Secrets foram utilizados para separar configurações e
credenciais do código da aplicação.

Também foram implementadas verificações de saúde utilizando readiness e
liveness probes, permitindo que o Kubernetes monitore o estado dos
containers.

------------------------------------------------------------------------

## Estratégia de deploy

A estratégia de implantação adotada foi o Rolling Update, que é o
comportamento padrão do Kubernetes para Deployments.

Essa estratégia permite atualizar uma aplicação gradualmente,
substituindo os pods antigos por novos sem causar indisponibilidade do
serviço.

------------------------------------------------------------------------

## Escalabilidade

A arquitetura foi projetada para permitir escalabilidade horizontal dos
serviços HTTP, principalmente gateway e pedidos.

Em um ambiente real seria possível utilizar o Horizontal Pod Autoscaler
(HPA) para aumentar ou diminuir automaticamente o número de pods de
acordo com o consumo de CPU ou memória.

------------------------------------------------------------------------

## Observabilidade

Embora não tenha sido implementado completamente neste MVP, a
arquitetura foi pensada para suportar ferramentas modernas de
observabilidade.

As métricas poderiam ser coletadas utilizando Prometheus e visualizadas
através do Grafana.

Logs dos containers poderiam ser centralizados utilizando ferramentas
como Loki ou Elasticsearch.

Para rastreamento distribuído entre os microserviços, uma solução como
OpenTelemetry e Jaeger poderia ser integrada ao sistema.

------------------------------------------------------------------------

## CI/CD

Como evolução natural do projeto, seria possível implementar um pipeline
de integração contínua que realizasse automaticamente o build das
imagens Docker, execução de testes e preparação do deploy para o cluster
Kubernetes.

Ferramentas como GitHub Actions ou GitLab CI poderiam ser utilizadas
para automatizar esse processo.

------------------------------------------------------------------------

## Vídeo demonstrativo

O vídeo demonstrando a arquitetura e a execução do sistema será
disponibilizado no seguinte link:

(adicionar link do vídeo aqui)

------------------------------------------------------------------------

## Conclusão

Este projeto demonstra como uma aplicação monolítica pode ser
reorganizada em microserviços e implantada utilizando práticas modernas
de DevOps.

Mesmo sendo um MVP simplificado, ele ilustra conceitos importantes como
conteinerização, orquestração, isolamento de serviços, gerenciamento de
configuração e preparação para escalabilidade em ambientes cloud-native.
