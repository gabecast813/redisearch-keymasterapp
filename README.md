# 🧭 Redisearch JSON User API

A lightweight **FastAPI** microservice that uses **Redis Stack / Redis Cloud** with **RediSearch on JSON data** to search users by attributes such as `user_type`, `id`, or other fields.

This service demonstrates how to:
- Store structured JSON user records in Redis (`user:id:<number>`)
- Build a **RediSearch index** on JSON fields  
- Query data efficiently with tag, numeric, and text filters  
- Run the entire stack in Docker on **port 8090**

---

## 🚀 Features

✅ JSON data modeling in Redis  
✅ Full RediSearch indexing (`idx:users`)  
✅ Prefix-based key pattern (`user:id:`)  
✅ Filter by `user_type` (`internal`, `external`, or both)  
✅ Filter by numeric `id`  
✅ Optional sample data loader  
✅ Connects directly to **Redis Cloud**  
✅ Runs cleanly with **Docker Compose**

---

## 🧩 Tech Stack

| Component | Purpose |
|------------|----------|
| **FastAPI** | Lightweight REST API |
| **Redis Cloud / Redis Stack** | JSON storage + RediSearch |
| **RedisJSON** | Structured JSON storage |
| **RediSearch** | Fast indexing and querying |
| **Docker Compose** | Container orchestration |

---

## ⚙️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)  
- A **Redis Cloud** instance  
  (Sign up for free at [https://redis.io/try-free/](https://redis.io/try-free/))

---

## 🧱 Project Structure
redisearch-service/
├── app/
│   ├── main.py             # FastAPI app and endpoints
│   ├── redis_client.py     # Redis Cloud connection and index setup
│   ├── data_loader.py      # Loads sample JSON users
│   └── models.py           # Pydantic models for API responses
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md

---

## ⚡ Quick Start

### 1️⃣ Configure your Redis Cloud credentials
Create a `.env` file in the project root:

```bash
REDIS_HOST=redis-19312.c80.us-east-1-2.ec2.redns.redis-cloud.com
REDIS_PORT=19312
REDIS_PASSWORD=your_redis_cloud_password_here

2️⃣ Build and start the container
docker compose up --build
🛠️ Creating RediSearch index...
✅ Index created successfully.
✅ Loaded Aaron Black (user:id:368)
✅ Loaded Jon Snow (user:id:369)
Uvicorn running on http://0.0.0.0:8090

✅ The API is now live at:
http://localhost:8090

3️⃣ Explore the API documentation
http://localhost:8090/docs

4️⃣ Try querying the API
curl -s "http://localhost:8090/v1/redisearch/users?user_type=internal" | jq

curl -s "http://localhost:8090/v1/redisearch/users?user_type=external" | jq

curl -s "http://localhost:8090/v1/redisearch/users?user_type=internal|external" | jq

curl -s "http://localhost:8090/v1/redisearch/users?id=368" | jq

🧠 Example JSON Schema

Each user document stored in Redis:
{
  "id": 368,
  "username": "aablack0",
  "first_name": "Aaron",
  "last_name": "Black",
  "email": "aablack0@example.com",
  "display_name": "Aaron Black",
  "user_type": "internal"
}


Key format in Redis:
user:id:368

🔍 RediSearch CLI Queries

If you connect via redis-cli (or RedisInsight):

FT.SEARCH idx:users "@user_type:{internal}"
FT.SEARCH idx:users "@user_type:{external}"
FT.SEARCH idx:users "@user_type:{internal|external}"
FT.SEARCH idx:users "@id:[368 368]"

🧰 Docker Commands
Action
Command
Restart container
docker compose restart redisearch
Stop container
docker compose down
View logs
docker logs redisearch-service
Open a shell inside the container
docker exec -it redisearch-service bash
Check Redis Cloud keys
redis-cli -h $REDIS_HOST -a $REDIS_PASSWORD -p $REDIS_PORT keys "user:id:*"


💡 Development Notes
	•	The RediSearch index is automatically created on startup (init_index()).
	•	JSON keys are stored with the prefix user:id:.
	•	Index name: idx:users
	•	Sample data is auto-loaded from data_loader.py.

To skip loading data (if your Redis Cloud already has user data), comment out this line in main.py:

load_data()

🧩 Example Output in Console
redisearch-service-1  | 🛠️ Creating RediSearch index...
redisearch-service-1  | ✅ Index created successfully.
redisearch-service-1  | ✅ Loaded Aaron Black (user:id:368)
redisearch-service-1  | ✅ Loaded Jon Snow (user:id:369)
redisearch-service-1  | INFO:     Uvicorn running on http://0.0.0.0:8090
redisearch-service-1  | INFO:     Application startup complete.

🧪 Health Check

Once running:
curl -s http://localhost:8090/health | jq
		or
Use browser: http://localhost:8090/health


🧱 Future Enhancements
	•	Add q parameter for free-text search
	•	Add pagination (limit + cursor)
	•	Add multi-field combined search (e.g. by user_type + first_name)
	•	Add POST endpoint for inserting new users

⸻

📜 License

MIT License © 2025
Created with ❤️ using FastAPI and Redis Stack



