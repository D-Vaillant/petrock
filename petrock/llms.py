# from openai import OpenAI
# import guidance

import tiktoken
from guidance import models
from llama_cpp import Llama
from openai import OpenAI

from pathlib import Path
import logging
import os
# from petrock.models import get_model_zoo
SERVER_PORT = os.getenv("SERVER_PORT", "8080")
SERVER_URL = f"http://localhost:{SERVER_PORT}/v1"

# # LlamaCpp LLM
# def create_llm(model_name: str, echo=False,
#               **llama_kwargs) -> models.LlamaCpp:
#     logging.debug(f"Retrieving {model_name}.")
#     zoo = get_model_zoo()
#     try:
#         model_data: str = zoo[model_name]
#     except KeyError:
#         raise Warning(f"Couldn't find model: {model_name}")
#     del model_data['chat_format']
#     base = Llama(model_data['model'], **model_data)
#     return models.LlamaCppChat(base, echo=echo)


# API LLMs
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