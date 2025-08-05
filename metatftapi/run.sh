#!/bin/bash

if [ ! -f ".env" ];then
    cp .env.example .env
fi

uv sync
uv pip install dotenv requests
uv run parse.py