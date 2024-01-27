#!/bin/bash

source venv/bin/activate

redis-server /app/config/redis.conf &

ls -la 

cd secrets

ls -la

cd service-account

ls -la

cd ..

cd ..

uvicorn app.main:app --host 0.0.0.0 --port 8000