#!/bin/bash

source venv/bin/activate

redis-server /app/config/redis.conf &

ls -la 

ls -la secrets

ls -la secrets/service-account

uvicorn app.main:app --host 0.0.0.0 --port 8000