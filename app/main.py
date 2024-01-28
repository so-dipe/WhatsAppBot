from fastapi import FastAPI, Request
from config.config import Config
from app.whatsapp.whatsapp_client import WhatsAppClient
from app.language_models.google.google_chat_model import GoogleChatModel
from app.language_models.google.gemini import GeminiChatModel
from app.redis.redis_client import RedisClient
from .main_utils import is_message_old, process_incoming_message

VERIFY_TOKEN = Config.VERIFY_TOKEN
whatsapp_client = WhatsAppClient()
redis_client = RedisClient()

app = FastAPI()

#use /webhook when in production mode
@app.get("/webhook")
def subscribe(request: Request):
    print("subscribe is being called")
    if request.query_params.get('hub.verify_token') == VERIFY_TOKEN:
        return int(request.query_params.get('hub.challenge'))
    return "Authentication failed. Invalid Token."

#use /webhook/ when in dev and prod.
@app.post("/webhook/")
async def callback(request: Request):
    print("callback is being called")
    body = await request.json()
    payload = whatsapp_client.process_payload(body)
    if len(payload) > 0:
        for message in payload:
            if is_message_old(message):
                print("Message is too old. Ignoring...")
                continue

            reply = await process_incoming_message(message)

            if reply:
                whatsapp_client.reply_message(message['from'], message['id'], reply)
                print(f"Reply sent to {message['from']}")
    return {"status": "success"}, 200