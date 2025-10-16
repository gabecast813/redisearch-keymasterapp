import json
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from .models import User, SearchResponse
from .redis_client import r, init_index
from .data_loader import load_data
from redis.commands.search.query import Query as RedisQuery
from redis.exceptions import RedisError

app = FastAPI(title="Redisearch JSON User API", version="1.3")

@app.on_event("startup")
def startup():
    init_index()
    load_data()  # Comment out if Redis already has data


# ✅ Health Check Endpoint
@app.get("/health", summary="Check API and Redis health")
def health_check():
    """
    Returns 200 OK if the FastAPI app and Redis connection are healthy.
    """
    try:
        r.ping()
        redis_status = "connected"
    except RedisError as e:
        redis_status = f"error: {str(e)}"

    status = {
        "status": "ok" if redis_status == "connected" else "degraded",
        "service": "redisearch-json-user-api",
        "redis": redis_status,
    }
    return JSONResponse(content=status, status_code=200)


# ✅ Search endpoint
@app.get("/v1/redisearch/users", response_model=SearchResponse)
def search_users(
    id: int | None = Query(None, description="Numeric ID match"),
    user_type: str | None = Query(None, description="Exact match for user_type"),
):
    """Search users by user_type or numeric ID using RediSearch JSON."""
    if id is not None:
        query_str = f"@id:[{id} {id}]"
    elif user_type:
        query_str = f"@user_type:{{{user_type}}}"
    else:
        query_str = "*"

    results = r.ft("idx:users").search(RedisQuery(query_str))

    users = []
    for doc in results.docs:
        user_data = json.loads(doc.json)
        users.append(User(**user_data))

    return SearchResponse(users=users, count=results.total)
