#!/bin/bash

# export FLASK_ENV=development

# Create a new screen session
screen -dmS petrock

screen -S petrock -X screen -d -m -t "flask" flask run
screen -S petrock -X screen -d -m -t "llama" python -m llama_cpp.server --config petrock/server_config.json

# Attach to the screen session
screen -r petrock
