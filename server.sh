#!/bin/sh
# Best to run this in a screen/tmux window.

python -m llama_cpp.server --config petrock/server_config.json

export FLASK_APP=app.py
export FLASK_ENV=development
poetry run flask run --host=0.0.0.0