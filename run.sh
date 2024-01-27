#!/bin/bash

source venv/bin/activate

redis-server /app/config/redis.conf &

ls -la & cd secrets & ls -la

uvicorn app.main:app --host 0.0.0.0 --port 8000