#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

uv venv

source .venv/bin/activate

uv pip install .

python manage.py migrate
