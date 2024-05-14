from pathlib import Path
from huggingface_hub import hf_hub_download


MODELS = [
    ('bartowski/Meta-Llama-3-8B-Instruct-GGUF', 'Meta-Llama-3-8B-Instruct-IQ3_XXS.gguf'),
    ('bartowski/Meta-Llama-3-8B-Instruct-GGUF', 'Meta-Llama-3-8B-Instruct-Q3_K_M.gguf'),
    ('vikhyatk/moondream2', 'moondream2-mmproj-f16.gguf'),
    ('vikhyatk/moondream2', 'moondream2-text-model-f16.gguf')
]

for REPO_ID, FILENAME in MODELS:
    if not (Path('models')/FILENAME).exists():
        print(f"Downloading {FILENAME}...")
        hf_hub_download(repo_id=REPO_ID, filename=FILENAME, local_dir='models')
    else:
        print(f"{FILENAME} already downloaded.")