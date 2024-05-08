# from openai import OpenAI
# import guidance
import tiktoken
from guidance import models
from openai import OpenAI

import os
SERVER_PORT = os.getenv("SERVER_PORT", "8080")
SERVER_URL = f"http://localhost:{SERVER_PORT}/v1"


def summon_llm(model_name, echo=False) -> models.OpenAI:
    llm = models.OpenAIChat(model=model_name, api_key='petrock',
                        tokenizer=tiktoken.get_encoding('cl100k_base'),
                        base_url=SERVER_URL, echo=echo)
    return llm


def summon_moondream() -> OpenAI:
    # Returns an OpenAI model.
    llm = OpenAI(model="moondream2",
                 api_key='moondream',
                 tokenizer=tiktoken.get_encoding('cl100k_base'),
                 base_url=SERVER_URL)
    return llm