#!/bin/bash

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="$HOME/.local/bin:$PATH"

python -m venv .venv

source .venv/bin/activate

uv pip install .

python manage.py migrate
