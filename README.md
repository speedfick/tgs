# Simulador - API, Sensor e Website

Este projeto é composto por três componentes:

- **API**: Backend principal
- **Sensor**: Microserviço de simulação de sensores
- **Website**: Frontend da aplicação

As imagens Docker são publicadas automaticamente para o **GitHub Container Registry (GHCR)**.

---

## 📦 Build e Push das Imagens

As imagens são construídas e publicadas automaticamente através de **GitHub Actions** quando há mudanças em:

| Componente | Caminho de build | Imagem publicada |
|:-----------|:-----------------|:-----------------|
| API        | `./api`           | `ghcr.io/speedfick/simulador-api:latest` |
| Sensor     | `./sensor`        | `ghcr.io/speedfick/simulador-sensor:latest` |
| Website    | `./website`       | `ghcr.io/speedfick/simulador-website:latest` |

---


### Fazer build das imagens dos diferentes serviços

`
docker build -t ghcr.io/speedfick/website:latest ./website
`
`
docker build -t ghcr.io/speedfick/sensor:latest ./sensor
`
`
docker build -t ghcr.io/speedfick/api:latest ./api
`
`

### Fazer push das imagens dos diferentes serviços para o ghcr

`
docker push ghcr.io/speedfick/api:latest
`
`
docker push ghcr.io/speedfick/sensor:latest
`
`
docker push ghcr.io/speedfick/website:latest
`

## 🚀

# Minikube
`https://minikube.sigs.k8s.io/docs/start`

### Iniciar o minikube (servidor kubernetes)
`minikube start --driver=docker`

### Outros comandos
`
minikube start 
`
`
minikube stop
`
`
minikube status
`
`
minikube delete
`

# Kubernetes (Cluster)
### Criação do namespace

`
kubectl create namespace production
`

### Aplicar ou atualizar recursos no Kubernetes / alterações apartir do ficheiro kustomization (-k)
### Dentro da respetiva pasta

`
kubectl apply -k 
`
### Apagar recursos no Kubernetes / alterações apartir do ficheiro kustomization (-k)
### Dentro da respetiva pasta 
`
kubectl delete -k .
`

### Verificar os pods em execução

`
kubectl get pods
`

### Verificar os serviços

`
kubectl get services
`

### Verificar os deployments

`
kubectl get deployments
`

### Instalar o NGINX - Ingress Controller

`
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
`

### Verificar o Status do Ingress Controller

`
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
`

### Verificar o Status do Ingress Controller

`
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
`

### Testar o serviço diretamente (sem Ingress)

`
kubectl port-forward svc/website-service 8081:80
`

### Testar o serviço diretamente (com Ingress)
`
kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx
`