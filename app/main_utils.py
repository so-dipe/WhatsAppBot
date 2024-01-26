from datetime import datetime, timedelta
from app.whatsapp.whatsapp_client import WhatsAppClient
from app.redis.redis_client import RedisClient
from app.language_models.google.google_chat_model import GoogleChatModel
from app.language_models.google.gemini import GeminiChatModel

whatsapp_client = WhatsAppClient()
redis_client = RedisClient()

chat_models = [
    GoogleChatModel(),
    GeminiChatModel(),
]

def is_message_old(message):
    now = datetime.now()
    timestamp = datetime.fromtimestamp(int(message['timestamp']))
    difference = now - timestamp
    return difference > timedelta(minutes=5)

def get_chat_model(redis_client, message, chat_models):
    model_name = redis_client.get_model_name(message['from'])
    print(model_name)
    if model_name == "gemini-pro-vision":
        return chat_models[1]
    elif model_name == "chat-bison@001":
        return chat_models[0]
    else: 
        return None

async def process_incoming_message(message):
    chat_model = get_chat_model(redis_client, message, chat_models)
    print(chat_model)
    if chat_model:
        chat_session = chat_model.get_history(message['from'])
        if message['type'] == 'image':
            reply = await process_image_message(chat_model, chat_session, message)
        elif message['type'] == 'text':
            if message['text'].startswith("/"):
                reply = process_special_commands(message)
            else:
                reply =  await chat_model.get_async_chat_response(chat_session, message['text'])
        chat_model.save_history(message['from'], chat_session)

        if message['type'] == 'button':
            reply = process_button_message(message)
    else:
        if message['type'] == 'button':
            reply = process_button_message(message)
        else:
            reply = "Sorry, you need to select a model to chat with."
            whatsapp_client.send_template_message(message['from'], "welcome_message")
    return reply


async def process_image_message(chat_model, chat_session, message):
    if message['caption'] is None:
        message['caption'] = "Explain this image."
    reply = await chat_model.get_async_chat_response(chat_session, message['caption'], message['media_bytes'])
    return reply


def process_special_commands(message):
    if "reset" in message['text'].lower():
        whatsapp_client.send_template_message(message['from'], "welcome_message")
        redis_client.delete_data(message['from'])

def process_button_message(message):
    if message['text'] == "get-started (default)":
        _ = chat_models[0].get_history(message['from'])
        reply = "Starting chat with google chat bison"
        print("starting chat with google chat bison")
    elif message['text'] == "gemini-pro-vision (beta)": 
        _ = chat_models[1].get_history(message['from'])
        reply = "Starting chat with gemini pro vision"
        print("starting chat with gemini pro vision")
    return reply