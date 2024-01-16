from fastapi import FastAPI, Request
from config.config import Config
from whatsapp.whatsapp_client import WhatsAppClient

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
            reply = f"Hi, You sent: {message['message']['text']}"
            whatsapp_client.send_message(message['from']['id'], reply)
            print(f"Reply sent to {message['from']['id']}")

    return {"status": "success"}, 200