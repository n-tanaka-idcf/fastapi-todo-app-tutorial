#!/bin/bash

uv run python -m api.migrate_db

uv run fastapi dev api/main.py
