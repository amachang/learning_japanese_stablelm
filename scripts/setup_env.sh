#!/bin/bash

set -eu

python3.10 -m venv venv
venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
