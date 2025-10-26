import asyncio
import os

import redis
from beanie import init_beanie
from flask import Flask
from flask.cli import load_dotenv
from pymongo import AsyncMongoClient

from logger import init_logger
from models.configuration import Configuration

mongodb_client = None
redis_db = None

logger = init_logger("rex-radio.daemon.api")

app = Flask(__name__)

def run(host="0.0.0.0", port=5000):
    global mongodb_client, redis_db

    logger.info(f"Starting API server on {host}:{port}")

    # dotenv
    logger.info("🔌 Loading .env")
    load_dotenv()
    logger.info("✅ .env loaded")

    # Redis
    logger.info("🔌 Connecting to Redis")
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_auth = os.getenv("REDIS_AUTH", "")

    redis_db = redis.Redis(host=redis_host, port=redis_port, password=redis_auth, db=0)

    logger.info(f"✅ Connected to Redis")

    # MongoDB Init
    mongodb_uri = os.getenv("MONGO_URI", "")

    logger.info(f"🔌 Connecting to MongoDB")
    logger.info(f"T {mongodb_uri}")

    async def init_mongo():
        global mongodb_client
        mongodb_client = AsyncMongoClient(mongodb_uri)
        db = mongodb_client.get_default_database()

        await init_beanie(database=db, document_models=[Configuration])


    # Initialize MongoDB before running Flask
    asyncio.run(init_mongo())

    logger.info("✅ Connected to MongoDB")

    app.run(host=host, port=port)
