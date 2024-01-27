#!/bin/bash

source venv/bin/activate

ls -la

cd secrets && ls -la && cd ..

uvicorn app.main:app --host 0.0.0.0 --port 8000