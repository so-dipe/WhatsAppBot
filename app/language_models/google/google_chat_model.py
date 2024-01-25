from vertexai.language_models import ChatModel, ChatSession, ChatMessage
from vertexai.vision_models import ImageTextModel, Image
from ...redis.redis_client import RedisClient
import os
from .setup import initialize_vertexai

initialize_vertexai()

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'assets/system-prompt.txt')

redis_client = RedisClient()

chat_model = ChatModel.from_pretrained("chat-bison@001")
image_model = ImageTextModel.from_pretrained("imagetext@001")

with open(file_path, "r") as f:
    system_prompt = f.read()

def init_chat():
    chat = chat_model.start_chat(context=system_prompt)
    return chat

def get_chat_response(chat, prompt, image=None):
    if image:
        image = Image(image)
        response = image_model.get_captions(image)[0]
        chat._message_history.extend(
            [
                ChatMessage(content="Given the image, what do you see", author="user"),
                ChatMessage(content=f"I see: {response}", author="bot"),
            ]
        )
        response = chat.send_message(prompt).text
    else:
        response = chat.send_message(prompt).text
    return response

def save_history(chat_id, chat_session: ChatSession):
    history = chat_session.message_history
    redis_client.save_chat_session(chat_id, history)

def get_history(chat_id):
    chat_session = init_chat()
    history = redis_client.get_chat_session(chat_id)
    if history is False:
        save_history(chat_id, chat_session)
    else:
        chat_session._message_history = history
    return chat_session