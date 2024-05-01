#!/bin/bash

# download_ggufs.sh
# 	Downloads the GGUF files for LlamaCpp.
urls=("https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF/resolve/main/Meta-Llama-3-8B-Instruct-IQ3_XXS.gguf")
	#  "https://huggingface.co/vikhyatk/moondream2/resolve/main/moondream2-mmproj-f16.gguf",
	#  "https://huggingface.co/vikhyatk/moondream2/resolve/main/moondream2-text-model-f16.gguf")


# Iterate through each URL
for url in "${urls[@]}"
do
  # Extract the filename from the URL
  filename=$(basename "$url")

  # Check if the file exists
  if [ ! -f "$filename" ]; then
    # File doesn't exist, download it using wget
    wget "$url"
    echo "Downloaded: $filename"
  else
    echo "File already exists: $filename"
  fi
done

"
