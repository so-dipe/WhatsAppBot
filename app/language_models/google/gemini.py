from vertexai.preview.generative_models import GenerativeModel, Image, ChatSession
from ...redis.redis_client import RedisClient
from .setup import initialize_vertexai
from ..chat_model import ChatModel

class GeminiChatModel(ChatModel):
    def __init__(self, model_name="gemini-pro-vision"):
        initialize_vertexai()
        self.redis_client = RedisClient()
        self.model = GenerativeModel(model_name)

    def init_chat(self):
        chat = self.model.start_chat()
        return chat

    def get_chat_response(self, chat: ChatSession, prompt: str, image=None) -> str:
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

    def save_history(self, chat_id, chat_session):
        history = chat_session.history
        self.redis_client.save_chat_session(chat_id, history)

    def get_history(self, chat_id):
        chat_session = self.init_chat()
        history = self.redis_client.get_chat_session(chat_id)
        if history is False:
            self.save_history(chat_id, chat_session)
        else:
            chat_session._history = history
        return chat_session