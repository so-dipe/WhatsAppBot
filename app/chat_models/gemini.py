import vertexai
from vertexai.preview.generative_models import GenerativeModel, Content, Part, Image, ChatSession
from config.config import Config
import json
from google.oauth2 import service_account

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
