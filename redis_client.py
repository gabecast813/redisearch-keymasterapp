import os
import redis
from redis.commands.search.field import TextField, TagField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

# Redis Cloud connection
REDIS_HOST = os.getenv("REDIS_HOST", "redis-19312.c80.us-east-1-2.ec2.redns.redis-cloud.com")
REDIS_PORT = int(os.getenv("REDIS_PORT", 19312))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Create Redis client
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)

def init_index():
    """Initialize the RediSearch index for JSON documents."""
    try:
        r.ft("idx:users").info()
        print("✅ Index already exists.")
    except:
        print("🛠️ Creating RediSearch index...")
        schema = [
            NumericField("$.id", as_name="id"),
            TextField("$.username", as_name="username"),
            TextField("$.first_name", as_name="first_name"),
            TextField("$.last_name", as_name="last_name"),
            TextField("$.email", as_name="email"),
            TextField("$.display_name", as_name="display_name"),
            TagField("$.user_type", as_name="user_type"),
        ]
        r.ft("idx:users").create_index(
            schema,
            definition=IndexDefinition(prefix=["user:id:"], index_type=IndexType.JSON),
        )
        print("✅ Index created successfully.")