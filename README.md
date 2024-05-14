# petrock
Make your Raspberry Pi, into a pet rock. That can see.

## Installation
You need `poetry`.

Run:
`poetry install`

To download the requisite models, run:
`poetry run ./download_models.py`

Then, to run the server:
`poetry run ./server.sh`

This starts `screen` with both `flask` and `llama_cpp.server` running. You can access the server at port 5050 - localhost:5050 if running locally.

## Deployment

### Raspberry Pi
First, you need poetry and screen:
`sudo apt install python3-poetry screen`

Then install as normal.

### Troubleshooting
Sometimes you'll run into a DBus error when trying to use `poetry`. Do this, and `source ~/.bashrc`, and things should work properly.
`echo "export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring" >> ~/.bashrc`

## Architecture
Petrock is run through a Flask app that communicates with `llama_cpp.server` using the configuration found under `petrock/server_config.json`.

This server serves the Moondream2 VLM and a quantized LLama3 LLM.