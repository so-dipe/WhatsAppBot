#!/bin/bash

source venv/bin/activate

redis-server &

ls -l

cd secrets

ls -l

cd whatsapp-bot

ls -l

cd ..
cd ..

uvicorn app.main:app --host 0.0.0.0 --port 8000