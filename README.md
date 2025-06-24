# 🔗 URL Shortener Service (Python + Redis + PostgreSQL)

A production-grade URL shortener service inspired by systems like Bit.ly or TinyURL. This service allows users to convert long URLs into short, unique links and handles redirection with high performance using Redis caching and persistent storage with PostgreSQL.

---

## 🛠️ Features

- 🔑 Shorten long URLs using random Base62 strings
- 🚀 Fast redirection via Redis caching (cache-aside pattern)
- 💾 Persistent storage in PostgreSQL
- ♻️ Collision-safe random string generation
- 🕒 Optional link expiration support
- 📈 Optional analytics: click tracking, timestamping
- 🐳 Dockerized and deployable infrastructure
- 🧪 Designed for scale and extensibility

---

## 📦 Tech Stack

| Layer            | Technology         |
|------------------|--------------------|
| Web Framework     | FastAPI / Flask    |
| Language          | Python             |
| Cache             | Redis              |
| Database          | PostgreSQL         |
| Containerization  | Docker             |
| Infra as Code     | Terraform (optional) |
| Web Server        | NGINX + Gunicorn   |
| Hosting           | AWS / Render / Railway |

---


## 🧱 Core Components

### 1. Random Short Code Generator
- Uses a secure RNG to generate a **6–8 character Base62 string**
- Ensures uniqueness via atomic **insert into DB**
- Retries on collision (very rare)

### 2. Redis Caching (Cache-aside)
- Fast lookup of hot `short_code`s
- TTL to auto-evict old or cold entries
- Reduces load on primary DB

### 3. PostgreSQL Storage
- Stores mapping: `short_code`, `long_url`, timestamps
- Enforces uniqueness with constraints
- Optional support for expiration

---

## 📄 API Endpoints

### `POST /shorten`
- Input: `{ "long_url": "https://example.com" }`
- Output: `{ "short_url": "https://short.ly/abc123" }`

### `GET /{short_code}`
- Redirects to the original long URL (302)
- Cached in Redis for fast repeated access

### `GET /analytics/{short_code}` _(Optional)_
- Returns: creation time, click count, expiry info

---

## 📋 Database Schema

| Column       | Type         | Description                  |
|--------------|--------------|------------------------------|
| id           | UUID / INT   | Primary key                  |
| short_code   | VARCHAR(10)  | Unique, Base62 string        |
| long_url     | TEXT         | Original URL                 |
| created_at   | TIMESTAMP    | Link creation time           |
| expires_at   | TIMESTAMP    | (Optional) expiry time       |
| click_count  | INT          | (Optional) for analytics     |

---

## 🔧 Logic Flow (Simplified)

### Shortening:
1. Receive `long_url`
2. Generate random Base62 string
3. Attempt DB insert (unique constraint)
4. Retry on collision
5. Return full short URL

### Redirection:
1. Lookup `short_code` in Redis
2. If miss, query DB and populate Redis
3. Redirect with HTTP 302

---

## 🧪 Development Instructions

1. 🧰 Create virtual environment
2. 📦 Install dependencies (`FastAPI`, `redis-py`, `psycopg2`, etc.)
3. 🛠️ Setup `.env` for Redis and DB config
4. 📂 Implement:
   - URL validation
   - Base62 string generation
   - Redis cache-aside logic
   - PostgreSQL insert/query logic
5. 🔁 Test shortening & redirection endpoints

---

## 🐳 Docker Deployment

### Docker Compose Stack:
- `app`: Python + Gunicorn
- `redis`: In-memory cache
- `postgres`: Persistent DB
- `nginx`: Reverse proxy

```bash
docker-compose up --build