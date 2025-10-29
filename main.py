import os
from multiprocessing import Process
from typing import Optional

from gpt4all import GPT4All
from llama_cpp import Llama


def run():
    MODEL_PATH = "llms/phi-4-Q4_0.gguf"
    # os.makedirs("models", exist_ok=True)

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=16000,
        n_threads=4,  # adjust for your CPU cores
    )

if __name__ == "__main__":
    run()