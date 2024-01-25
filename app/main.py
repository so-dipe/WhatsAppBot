from fastapi import FastAPI, Request
from config.config import Config
from app.whatsapp.whatsapp_client import WhatsAppClient
from app.language_models.google.google_chat_model import get_chat_response, save_history, get_history
# from app.language_models.hugging_face.model import get_chat_response, save_history, get_history
from app.redis.redis_client import RedisClient

VERIFY_TOKEN = "verify"
whatsapp_client = WhatsAppClient()
redis_client = RedisClient()

app = FastAPI()

# chat_session = init_chat()

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
            chat_session = get_history(message['from'])
            if message['type'] == 'image':
                if message['caption'] is None:
                    message['caption'] = "Explain this image."
                reply = get_chat_response(chat_session, message['caption'], message['media_bytes'])
            elif message['type'] == 'text':        
                reply =  get_chat_response(chat_session, message['text'])
            else:
                continue
            save_history(message['from'], chat_session)
            whatsapp_client.reply_message(message['from'], message['id'], reply)
            print(f"Reply sent to {message['from']}")
    return {"status": "success"}, 200