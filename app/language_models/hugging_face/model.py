import requests
from config.config import Config
from ...redis.redis_client import RedisClient

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

redis_client = RedisClient()

class ChatSession:
    def __init__(self):
        self.past_user_inputs = []
        self.generated_responses = []
    
    def append_history(self, user_input, generated_response):
        self.past_user_inputs.append(user_input)
        self.generated_responses.append(generated_response)
    
    def get_history(self):
        return {
            "past_user_inputs": self.past_user_inputs,
            "generated_responses": self.generated_responses
        }

model_api_url = Config.HUGGINGFACE_MODEL_API_URL
hf_token = Config.HUGGINGFACE_TOKEN

def input_payload(history: ChatSession, message):
    return {
        "inputs": {
            "past_user_inputs": history.past_user_inputs,
            "generated_responses": history.generated_responses,
            "text": message
        }
        # "inputs": message
    }

def get_chat_response(history, message):
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = input_payload(history, message)
    try:
        response = requests.post(model_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            chat_response = response.json()
            return chat_response
        else:
            print(response.text)
            print("Failed to get chat response from Hugging Face.")
    except Exception as e:
        print(f"Error getting chat response from Hugging Face: {str(e)}")

def save_history(chat_id, chat_session):
    redis_client.save_chat_session(chat_id, chat_session)

def get_history(chat_id):
    chat_session = redis_client.get_chat_session(chat_id)
    if chat_session is False:
        chat_session = ChatSession()
        save_history(chat_id, chat_session)
    return chat_session

