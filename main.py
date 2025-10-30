import os
import asyncio
from multiprocessing import Process
from typing import Optional

from beanie import init_beanie
from dotenv import load_dotenv
from gpt4all import GPT4All
from llama_cpp import Llama
from pymongo import AsyncMongoClient

from logger import init_logger
from models.configuration import Configuration


# 1. Get station information
    # Name
    # Description
    # Genres
# 2. Generate radio schedule


logger = init_logger("rex-radio.daemon.api")

async def get_station_configuration():
    return await Configuration.find_all().to_list()


async def run():
    logger.info("🔌 Loading .env")
    load_dotenv()
    logger.info("✅ .env loaded")

    # MongoDB
    logger.info("🔌 Loading MongoDB")
    mongodb_uri = os.getenv("MONGO_URI", "")

    client = AsyncMongoClient(mongodb_uri)
    db = client["rex_radio"]
    await init_beanie(database=db, document_models=[Configuration])

    logger.info("✅ MongoDB connected")

    MODEL_PATH = "llms/phi-4-Q4_0.gguf"
    # os.makedirs("models", exist_ok=True)

    # Get Station Configuration
    configuration = await get_station_configuration()

    # TODO - Update this
    station_name = next((c.value for c in configuration if c.field == 'name'), None)
    station_description = next((c.value for c in configuration if c.field == 'description'), None)
    station_genres = next((c.value for c in configuration if c.field == 'genres'), [])

    print(station_name)

    # Search for information in the list of configuration
    station_name = configuration

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_gpu_layers=-1,
        n_threads=os.cpu_count(),
    )

    prompt = (
        "<|system|>\n"
        f"You are a radio script generator.\n"
        # f"Topic: {topic}. Style: {style}.\n"
        "<|end|>\n"
        "<|user|>\n<|assistant|>"
    )

    # Generate output
    # output = llm(prompt, max_tokens=256, stop=["<|end|>"])
    # print(output["choices"][0]["text"].strip())

if __name__ == "__main__":
    asyncio.run(run())