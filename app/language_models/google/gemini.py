from vertexai.preview.generative_models import GenerativeModel, Image, ChatSession
from ...redis.redis_client import RedisClient
from .setup import initialize_vertexai
from ..chat_model import ChatModel
import os


class GeminiChatModel(ChatModel):
    def __init__(self, model_name="gemini-pro-vision", system_prompt_file_path="assets/system-prompt.txt"):
        initialize_vertexai()
        self.model_name = model_name
        self.redis_client = RedisClient()
        self.model = GenerativeModel(model_name)
        if system_prompt_file_path:
            base_dir = os.path.dirname(__file__)
            system_prompt_file_path = os.path.join(base_dir, system_prompt_file_path)
            with open(system_prompt_file_path, "r") as f:
                self.system_prompt = f.read()

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
            prompt = f"<SYS> Context: {self.system_prompt} <SYS> \n Query: {prompt}"
            response = chat.send_message(prompt)
            try:
                response = chat.send_message(prompt).text
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                response = "sorry, an error occured."
        return response

    def save_history(self, chat_id, chat_session):
        history = chat_session.history
        model_name = "gemini-pro-vision"
        self.redis_client.save_data(chat_id, history, model_name)

    def get_history(self, chat_id):
        chat_session = self.init_chat()
        data = self.redis_client.get_data(chat_id)
        history = data['history']
        if (history is False) or (data['model_name'] != self.model_name):
            self.save_history(chat_id, chat_session)
        else:
            chat_session._history = history
        return chat_session