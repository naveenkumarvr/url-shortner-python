# URL Shortener

This is a simple URL shortener app. You provide a full URL, and it returns a shortened version. When you use the short URL, it redirects to the original one. Redis is used for in-memory caching.

## How to Deploy and Test

Follow the steps below to deploy this app.

---

### Prerequisites

- Docker / Docker Desktop installed on your computer

---

### 1. Create a Docker Network

All containers should be part of the same network:

```bash
docker network create url_shortner
```

---

### 2. Deploy MySQL Database

```bash
docker run --name mysql \
  -d \
  -e MYSQL_ROOT_PASSWORD=password \
  -p 3306:3306 \
  --network url_shortner \
  mysql
```

#### Create Database for the App

```bash
docker exec -it mysql /bin/bash
# Inside the container, run:
mysql -u root -p
# Enter password: password

# Inside MySQL shell:
CREATE DATABASE url_shortner;
```

---

### 3. Clone the Repo and Migrate Schema

```bash
git clone <your-repo-url>
cd url-shortner-python/app
pip install -r requirements.txt

# Initialize and migrate the database
flask db init
flask db migrate -m "Initial commit"
flask db upgrade
```

---

### 4. Deploy Redis

```bash
docker run --name redis \
  -d \
  -p 6379:6379 \
  --network url_shortner \
  redis:latest
```

---

### 5. Build and Run the App

```bash
# Build Docker image from Dockerfile
docker build -t urls:v1 .

# Run the container
docker run \
  -e MYSQL_HOST=mysql \
  -e REDIS_HOST=redis \
  -d \
  -p 8500:5000 \
  --name urls \
  --network url_shortner \
  urls:v1
```

---

### 6. Verify Containers

Make sure all containers (`mysql`, `redis`, `urls`) are running and healthy.

---

### 7. Test the App

**Create a short URL:**
```bash
curl -X POST http://localhost:8500/short \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://google.com"}'
```

**Use the short URL to redirect:**
```bash
curl -X GET http://localhost:8500/<SHORT_CODE>
```

---

**Note:**  
- Replace `<your-repo-url>` with your actual repository URL.
- Replace `<SHORT_CODE>` with the value you get from the previous command.

---