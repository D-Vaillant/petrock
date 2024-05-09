#!/bin/sh
# Best to run this in a screen/tmux window.

python -m llama_cpp.server --config petrock/server_config.json
