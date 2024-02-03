"""
This module is where the magic happens.

It contains the main FastAPI application instance and the route handlers
for the webhook.
"""

from fastapi import FastAPI, Request
from config.config import Config
from app.whatsapp.whatsapp_client import WhatsAppClient
from app.redis.redis_client import RedisClient
from .message_utils import is_message_old, process_incoming_message

VERIFY_TOKEN = Config.VERIFY_TOKEN
whatsapp_client = WhatsAppClient(RedisClient())

app = FastAPI()


@app.get("/webhook")
def subscribe(request: Request):
    """
    Sends a subscription request to the whatsapp webhook. This is a one-time
    verification process that happens when the webhook is first set up.
    It is required for the webhook to start receiving notifications from the
    whatsapp server.

    Args:
        request (Request): The incoming request object.

    Returns:
        int: The challenge code to verify the subscription request.
        str: A message indicating that the authentication failed.
    """
    print("subscribe is being called")
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(request.query_params.get("hub.challenge"))
    return "Authentication failed. Invalid Token."


@app.post("/webhook")
async def callback(request: Request):
    """
    This is the main route handler for the webhook. It processes incoming
    messages and sends replies to the whatsapp server.

    Args:
        request (Request): The incoming request object.

    Returns:
        dict: A dictionary containing the status of the request.
        int: The status code of the request.
    """
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
                whatsapp_client.reply_message(
                    message["from"], message["id"], reply
                )
                print(f"Reply sent to {message['from']}")
    return {"status": "success"}, 200
