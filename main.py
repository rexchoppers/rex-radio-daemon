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
    output = llm(prompt, max_tokens=256, stop=["<|end|>"])
    print(output["choices"][0]["text"].strip())

if __name__ == "__main__":
    run()