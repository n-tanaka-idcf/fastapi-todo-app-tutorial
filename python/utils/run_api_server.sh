#!/bin/bash
set -euo pipefail

uv run fastapi dev api/main.py
