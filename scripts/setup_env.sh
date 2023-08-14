#!/bin/bash

set -eu

cd ~

git clone git@github.com:amachang/learning_japanese_stablelm.git dev

cd ~/dev

python3.10 -m venv venv
venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
venv/bin/pip install transformers
venv/bin/pip install sentencepiece einops

# huggingface の authz がいるので access token を入れる
venv/bin/pip install huggingface_hub
venv/bin/huggingface-cli login

