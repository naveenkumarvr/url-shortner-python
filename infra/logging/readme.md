# Logging Setup

- Logging using promtail and loki and visvalization in grafana

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

kubectl create namespace logging


helm upgrade --install loki grafana/loki-stack \
  --namespace=logging \
  -f loki-values.yaml


```