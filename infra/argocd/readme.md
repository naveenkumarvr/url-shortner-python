# ArgoCD Setup Guide

This guide helps you install and configure ArgoCD on your Kubernetes cluster.

---

## 1. Install ArgoCD

See the [official docs](https://argo-cd.readthedocs.io/en/stable/getting_started/) for more details.

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
# Wait for the pods to be running
kubectl -n argocd get pods -w
```

---

## 2. Disable HTTPS (Force HTTP)

```bash
kubectl patch configmap argocd-cmd-params-cm -n argocd --type merge -p '{"data":{"server.insecure":"true"}}'
kubectl -n argocd rollout restart deploy argocd-server
```

---

## 3. Create Ingress for ArgoCD

```bash
kubectl apply -f argocd-ingress.yml
kubectl -n argocd get ingress
```

---

## 4. Get Admin Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

---

## 5. Login to ArgoCD UI

- URL: [http://argocd.localtest.me](http://argocd.localtest.me)
- Username: `admin`
- Password: (use the decoded password from the previous step)

---

## 6. ArgoCD CLI Setup & Password Reset

### Install ArgoCD CLI

```bash
curl -sSL -o argocd-linux-amd64 \
  https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64

sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd

argocd version --client
```

### Get Current Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

### Login to ArgoCD CLI

```bash
argocd login argocd.localtest.me --insecure --grpc-web
# --insecure: don't require HTTPS (HTTP is fine)
# --grpc-web: needed because NGINX ingress only passes gRPC-Web, not raw gRPC
```

### Reset the Password

```bash
argocd account update-password
```

---

## 7. Recover or Reset Lost Password

If you forget or lose the password:

```bash
# Delete the secret and let ArgoCD regenerate it:
kubectl -n argocd delete secret argocd-initial-admin-secret

# Restart the server:
kubectl -n argocd rollout restart deploy argocd-server

# Get the new password:
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

---

**Tip:**  
- Always keep your admin password safe.
- For production, consider enabling HTTPS and securing your ingress.

---

## Adding Helm repo
```bash
REPO_URL: http://192.168.0.102:9011/repository/helm-local/
```
- Considering you have helm-local as your local helm-hosted repo and is exposed to 9011. 
- Always use System/Node ip