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

## 🚀 Como testar localmente

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

### Criação do namespace

`
kubectl create namespace production
`

### Aplicar ou atualizar recursos no Kubernetes / alterações apartir do ficheiro kustomization (-k) 

`
kubectl apply -k k8s/
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



### 1. (Opcional) Fazer login no GHCR

**Só é necessário se a imagem for privada.**

```bash
echo $PAT_GHCR | docker login ghcr.io -u speedfick --password-stdin

2. Fazer Pull das Imagens
docker pull ghcr.io/speedfick/simulador-api:latest
docker pull ghcr.io/speedfick/simulador-sensor:latest
docker pull ghcr.io/speedfick/simulador-website:latest

3. Correr os containers localmente

API ->    docker run --rm -it -p 8080:8080 ghcr.io/speedfick/simulador-api:latest
Website ->   docker run --rm -it -p 3000:80 ghcr.io/speedfick/simulador-website:latest
Sensor ->    docker run --rm -it -p 8081:8081 ghcr.io/speedfick/simulador-sensor:latest

Aceder à API ->   http://localhost:8080
Aceder ao sensor ->   http://localhost:8081
Aceder ao website ->   http://localhost:3000
