#!/bin/bash

source venv/bin/activate

redis-server /app/config/redis.conf &

ls

ls secrets

cat secrets/service-account.json

uvicorn app.main:app --host 0.0.0.0 --port 8000