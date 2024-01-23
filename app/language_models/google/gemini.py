import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image, ChatSession
from config.config import Config
import json
from google.oauth2 import service_account
from ...redis.redis_client import RedisClient

redis_client = RedisClient()

with open(Config.SERVICE_ACCOUNT_PATH, "r") as f:
    credentials = json.load(f)
    credentials = service_account.Credentials.from_service_account_info(credentials)

vertexai.init(project=Config.GOOGLE_PROJECT_ID ,credentials=credentials)

model = GenerativeModel("gemini-pro-vision")

def init_chat():
    chat = model.start_chat()
    return chat

def get_chat_response(chat: ChatSession, prompt: str, image: Image = None) -> str:
    if image:
        image = Image.from_bytes(image)
        try:
            response = chat.send_message([prompt, image]).text
        except Exception as e:
            print(f"Error sending image: {str(e)}")
            response = "sorry, an error occured."
    else:
        response = chat.send_message(prompt)
        try:
            response = chat.send_message(prompt).text
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            response = "sorry, an error occured."
    return response

def save_history(chat_id, chat_session):
    history = chat_session.history
    redis_client.save_chat_session(chat_id, history)    

def get_history(chat_id):
    chat_session = init_chat()
    history = redis_client.get_chat_session(chat_id)
    if history is False:
        save_history(chat_id, chat_session)
    else:
        chat_session._history = history
    return chat_session