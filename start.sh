#!/usr/bin/env bash
echo "Starting FastAPI Portfolio Server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
