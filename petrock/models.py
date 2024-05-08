from pathlib import Path
import os
import logging
import json


import dotenv
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

dotenv.load_dotenv()

model_dir = os.getenv("MODEL_ZOO", 'models/')


def get_model(model_name: str,
              n_ctx: int = 2048,
              **llama_kwargs) -> Llama:
    logging.debug(f"Retrieving {model_name}.")
    zoo = get_model_zoo()
    try:
        model_path: Path = zoo[model_name]
    except KeyError:
        raise Warning(f"Couldn't find model: {model_name}")
    return Llama(model_path=str(model_path),
                 n_ctx=n_ctx,
                 n_gpu_layers=0,
                 **llama_kwargs)

def get_moondream() -> Llama:
    logging.debug(f"Retrieving Moondream OpenAI object.")
    chat_handler = Llava15ChatHandler(clip_model_path=f"{model_dir}/moondream2-mmproj-f16.gguf")
    llm = Llama(
        model_path=f"{model_dir}/moondream2-text-model-f16.gguf",
        chat_handler=chat_handler,
        n_ctx=2048, # n_ctx should be increased to accomodate the image embedding
        logits_all=True,# needed to make llava work
        n_gpu_layers=-1
    )
    return llm

def describe_image(llm: Llama, data_uri):
    return prompt_llm(llm,
        system_msg = "You are an assistant who perfectly describes images.",
        messages = [{"role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": data_uri }},
                            {"type" : "text", "text": "Describe this image in detail please."}
                        ]
                    }])

def prompt_llm(llm: Llama,
               system_msg: str = "You are a pet rock.",
               role: str = 'user',
               message: str = ''):
    system = {"role": "system", "content": system_msg}
    prompt = {"role": role, "content": message}
    # user_reply["content"] = {"type": "text", "text": message}

    r = llm.create_chat_completion(messages=[system, prompt])
    return r

def predict(llm, system_msg,
            message, history=None,
            **llm_kwargs):
    messages = [{"role": "system", "content": system_msg}]

    if history is None:
        history = []
    for user_message, assistant_message in history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": assistant_message})
    
    messages.append({"role": "user", "content": message})

    response = llm.create_chat_completion(
        messages=messages,
        # stream=True,
        **llm_kwargs
    )
    return response
    text = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            text += content
            yield text

def get_model_zoo():
    with open("petrock/server_config.json") as serverconfig_file:
        server_config = json.load(serverconfig_file)

    model_arr = server_config['models']
    zoo = {m['model_alias']: m for m in model_arr}
    for k in zoo:
        del zoo[k]['model_alias']
    return zoo


def print_model_zoo():
    ggufs = Path(model_dir).glob("*/*/*.gguf")  # List of GGUF files.
    for g in ggufs:
        print(g.stem)


if __name__ == "__main__":
    model_zoo = get_model_zoo()
    model_names = list(model_zoo.keys())
    name = model_names[7]
    llm = get_model(name)