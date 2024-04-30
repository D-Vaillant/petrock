from transformers import AutoModelForCausalLM, AutoTokenizer
from PIL import Image
from pathlib import Path

# Guidance
from guidance import image, user, assistant, gen, models


using = 'llamacpp'

# Moondream.
ggufs = list(Path('models').glob("*.gguf"))  # List of GGUF files.
model_zoo = {"llama3_iq3": "Meta-Llama-3-8B-Instruct-IQ3_XXS.gguf"}

if using == 'moondream':
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler

    chat_handler = Llava15ChatHandler(clip_model_path="models/moondream2-mmproj-f16.gguf")
    llm = Llama(
      model_path="models//moondream2-text-model-f16.gguf",
      chat_handler=chat_handler,
      n_ctx=2048,
      logits_all=True,# needed to make llava work
      n_gpu_layers=-1
    )
    lm = models.LlamaCppChat(llm)
elif using == 'llamacpp':
    # TODO: Model zoo.
    model_name = 'llama3_iq3'
    lm = models.LlamaCppChat(f"models/{model_zoo[model_name]}")


if __name__ == "__main__":
    with user():
        lm += "If you dream, what's next?"
    with assistant():
        lm += gen(stop='.', name='answer', max_tokens=25)
    print(lm['answer'])
