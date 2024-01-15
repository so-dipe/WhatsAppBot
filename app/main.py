from fastapi import FastAPI, HTTPException, Request
import requests
from config.config import Config

app = FastAPI()

VERIFY_TOKEN = "your_whatsapp_verify_token"

@app.post("/")
def index():
    return "welcome to app"

@app.get("/webhook/")
def subscribe(request: Request):
    print("subscribe is being called")
    if request.query_params.get('hub.verify_token') == VERIFY_TOKEN:
        return int(request.query_params.get('hub.challenge'))
    return "Authentication failed. Invalid Token."