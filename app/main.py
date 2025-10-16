import json
from fastapi import FastAPI, Query
from .models import User, SearchResponse
from .redis_client import r, init_index
from .data_loader import load_data
from redis.commands.search.query import Query as RedisQuery

app = FastAPI(title="Redisearch JSON User API", version="1.2")

@app.on_event("startup")
def startup():
    init_index()
    load_data()  # optional

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

    # ✅ Parse doc.json safely
    users = []
    for doc in results.docs:
        user_data = json.loads(doc.json)
        users.append(User(**user_data))

    return SearchResponse(users=users, count=results.total)