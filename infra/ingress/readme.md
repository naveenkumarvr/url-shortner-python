# Set up Ingress controller

```bash
# install Ingress
helm upgrade --install ingress-nginx ingress-nginx   --repo https://kubernetes.github.io/ingress-nginx   --namespace ingress-nginx --create-namespace

# Show the Deployed Helm
helm show values ingress-nginx --repo https://kubernetes.github.io/ingress-nginx
```

# Test Ingress Controller using sample app
```bash
kubectl create ns test-ing
kubectl apply -f deploy.yml -n test-ing
kubectl apply -f ingress.yml -n test-ing

# Once deployed use below command to test the ingress values
curl http://localhost
```