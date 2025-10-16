from .redis_client import r

SAMPLE_USERS = [
    {
        "id": 368,
        "username": "aablack0",
        "first_name": "Aaron",
        "last_name": "Black",
        "email": "aablack0@example.com",
        "display_name": "Aaron Black",
        "user_type": "internal",
    },
    {
        "id": 369,
        "username": "jsnow",
        "first_name": "Jon",
        "last_name": "Snow",
        "email": "jsnow@north.org",
        "display_name": "Jon Snow",
        "user_type": "external",
    },
]

def load_data():
    """Load sample users into Redis as JSON objects."""
    for user in SAMPLE_USERS:
        key = f"user:id:{user['id']}"
        r.json().set(key, "$", user)
        print(f"✅ Loaded {user['display_name']} ({key})")