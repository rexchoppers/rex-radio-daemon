import os

import redis
from flask import Flask

from logger import init_logger

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_auth = os.getenv("REDIS_AUTH", "")

redis_db = redis.Redis(host=redis_host, port=redis_port, db=0)

logger = init_logger("rex-radio.daemon.api")

app = Flask(__name__)

def run(host="0.0.0.0", port=5000):
    logger.info(f"Starting API server on {host}:{port}")
    app.run(host=host, port=port)