#!/bin/bash

source venv/bin/activate

redis-server &

uvicorn app.main:app --host 0.0.0.0 --port 8000