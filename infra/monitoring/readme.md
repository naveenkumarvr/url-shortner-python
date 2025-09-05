# Setup Promethus and grafana

- Make sure you have Ingress installed and enabled

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring

helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f values.yaml

kubectl get pods -n monitoring

```