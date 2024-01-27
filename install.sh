#!/bin/bash

apt-get update && apt-get install -y redis-server

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

