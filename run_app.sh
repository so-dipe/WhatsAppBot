#!/bin/bash

source venv/bin/activate

redis-server config/redis.conf &

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug 

