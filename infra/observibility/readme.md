# Observability

- Create Namespace
```bash
kubectl create ns observability
```

## Setup Jaeger
```bash
kubectl apply -f jaeger/jaeger.yml -n observability
kubectl apply -f jaeger/jaeger-ingress.yml -n observability
```

## Setup OTEL
```bash
kubectl apply -f otel/otel-collector.yml -n observability
```

## Testing App
```bash
kubectl create ns demo
kubectl apply -f sample-testapp/hotrod.yml -n 

kubectl port-foward -n demo service/hotrod 8888:8080
```