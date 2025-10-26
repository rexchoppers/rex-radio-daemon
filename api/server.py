import asyncio
import os

import redis
from beanie import init_beanie
from flask import Flask, request, jsonify
from flask.cli import load_dotenv
from pydantic import ValidationError
from pymongo import AsyncMongoClient

from api.requests.update_configuration_request import UpdateConfigurationRequest
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

    async def init_mongo():
        global mongodb_client
        mongodb_client = AsyncMongoClient(mongodb_uri)
        db = mongodb_client.get_default_database()

        await init_beanie(database=db, document_models=[Configuration])

    asyncio.run(init_mongo())
    logger.info("✅ Connected to MongoDB")

    logger.info("🤖 Finished initializing API server")

    logger.info("🚀 Application running")
    app.run(host=host, port=port)

@app.route("/config", methods=["PATCH"])
def update_configuration():
    try:
        # Expecting JSON to be an array of ConfigurationUpdate objects
        req_list = request.get_json(force=True)
        updates = [UpdateConfigurationRequest.parse_obj(item) for item in req_list]
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    async def apply_updates():
        for update in updates:
            config = await Configuration.find_one(Configuration.field == update.field)
            if config:
                await config.set({Configuration.value: update.value})
            else:
                await Configuration(field=update.field, value=update.value).insert()
        return True

    asyncio.run(apply_updates())

    return jsonify({"status": "ok"})