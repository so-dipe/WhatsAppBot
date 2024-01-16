from fastapi import FastAPI, Request
from config.config import Config
from app.whatsapp.whatsapp_client import WhatsAppClient

VERIFY_TOKEN = "your_whatsapp_verify_token"
whatsapp_client = WhatsAppClient()


app = FastAPI()

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
    print(body)
    response = whatsapp_client.process_notification(body)
    if len(response) > 0:
        for message in response:
            reply = f"Hi, You sent: {message['message']}"
            whatsapp_client.reply_message(message['sender_no'], message['id'],reply)
            print(f"Reply sent to {message['sender_no']}")

    return {"status": "success"}, 200