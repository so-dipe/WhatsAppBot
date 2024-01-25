from fastapi import FastAPI, Request
from config.config import Config
from app.whatsapp.whatsapp_client import WhatsAppClient
from app.language_models.google.google_chat_model import GoogleChatModel
from app.language_models.google.gemini import GeminiChatModel
from app.redis.redis_client import RedisClient
from datetime import datetime, timedelta
from .main_utils import is_message_old, get_chat_model, process_incoming_message

VERIFY_TOKEN = "verify"
whatsapp_client = WhatsAppClient()
redis_client = RedisClient()

app = FastAPI()

# chat_model = GoogleChatModel()

chat_models = [
    GoogleChatModel(),
    GeminiChatModel(),
]

@app.get("/webhook/")
def subscribe(request: Request):
    print("subscribe is being called")
    if request.query_params.get('hub.verify_token') == VERIFY_TOKEN:
        return int(request.query_params.get('hub.challenge'))
    return "Authentication failed. Invalid Token."

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
            
            chat_model = get_chat_model(redis_client, message, chat_models)
            # if message['type'] == 'image':
            #     if message['caption'] is None:
            #         message['caption'] = "Explain this image."
            #     reply = chat_model.get_chat_response(chat_session, message['caption'], message['media_bytes'])
            # elif message['type'] == 'text':        
            #     reply =  chat_model.get_chat_response(chat_session, message['text'])
            # elif message['type'] == 'button':
            #     if message['text'] == "get-started (default)":
            #         chat_session = chat_models[0].get_history(message['from'])
            #         print("starting chat with google chat bison")
            #     elif message['text'] == "gemini-pro-vision (beta)":
            #         chat_session = chat_models[1].get_history(message['from'])
            #         print("starting chat with gemini pro vision")
            # else:
            #     continue
            reply, chat_session = process_incoming_message(chat_model, chat_models, message)
            chat_model.save_history(message['from'], chat_session)
            whatsapp_client.reply_message(message['from'], message['id'], reply)
            # whatsapp_client.send_template_message(message['from'], "welcome_message")
            print(f"Reply sent to {message['from']}")
    return {"status": "success"}, 200