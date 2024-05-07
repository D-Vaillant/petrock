from pathlib import Path
import os

import dotenv
from PIL import Image
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

dotenv.load_dotenv()

model_dir = os.getenv("MODEL_ZOO", 'models/')


def get_model(model_name: str,
              n_ctx: int = 2048,
              **llama_kwargs) -> Llama:
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
               messages: list[dict] = None):
    system = {"role": "system", "content": system_msg}
    if messages is None:
        messages = dict()
    r = llm.create_chat_completion(messages=system + messages)
    return r


def get_model_zoo():
    ggufs = Path(model_dir).glob("*/*/*.gguf")  # List of GGUF files.
    model_zoo = {g.stem: g for g in ggufs}
    return model_zoo


def print_model_zoo():
    ggufs = Path(model_dir).glob("*/*/*.gguf")  # List of GGUF files.
    for g in ggufs:
        print(g.stem)


if __name__ == "__main__":
    model_zoo = get_model_zoo()
    model_names = list(model_zoo.keys())
    name = model_names[7]
    llm = get_model(name)