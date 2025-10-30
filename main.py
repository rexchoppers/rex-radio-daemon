import os
import asyncio
import time
from datetime import datetime
from multiprocessing import Process
from typing import Optional

from TTS.api import TTS
from beanie import init_beanie
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from gpt4all import GPT4All
from llama_cpp import Llama
from pymongo import AsyncMongoClient

from logger import init_logger
from models.configuration import Configuration
from radio_prompts import RadioPrompts

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
    print(station_genres)

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_gpu_layers=-1,
        n_threads=os.cpu_count(),
    )

    radio_prompts = RadioPrompts(
        station_name=station_name,
        personality="friendly",
        tone="upbeat"
    )


    # Generate output
    output = llm(radio_prompts.station_start_welcome_prompt(datetime.now().strftime("%-I:%M %p")), max_tokens=256, stop=["<|end|>"])
    response = output["choices"][0]["text"].strip()

    print(response)

    # Generate voice using TTS
    client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

    audio = client.text_to_speech.convert(
        text=response,
        voice_id="nrD2uNU2IUYtedZegcGx",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Save it
    with open("radio_intro.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)


if __name__ == "__main__":
    asyncio.run(run())