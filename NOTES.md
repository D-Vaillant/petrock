# Notes
Keep track of how things are going.

## VLMs
### Architecture
- NanoLLaVA: Doesn't easily work, because it requires flash attention and installing that on a Raspberry Pi is hard.
- Moondream: RAM requirements too high and no quantized models exist.
- Llama.cpp: This is what we'll do.

### Current Proposal: Hybrid Approach
- Use Moondream to encode images into text, and a quantized llama3 model. 

