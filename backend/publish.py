import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.from_url(os.getenv("REDIS_URL"))

redis_client.publish('events', json.dumps({
    'receivers': ['USER_ID'],
    'data': {
        'type': 'MESSAGE',
        'data': 'Hello World'
    },
    }))