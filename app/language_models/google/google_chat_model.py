from vertexai.language_models import ChatModel, ChatSession, ChatMessage
from vertexai.vision_models import ImageTextModel, Image
from ...redis.redis_client import RedisClient
import os
from .setup import initialize_vertexai
from ..chat_model import ChatModel as AbstractChatModel

class GoogleChatModel(AbstractChatModel):
    def __init__(self, model_name="chat-bison@001", image_model_name="imagetext@001", system_prompt_file_path="assets/system-prompt.txt"):
        initialize_vertexai()
        self.redis_client = RedisClient()
        self.chat_model = ChatModel.from_pretrained(model_name)
        if image_model_name:
            self.image_model = ImageTextModel.from_pretrained(image_model_name)
        if system_prompt_file_path:
            base_dir = os.path.dirname(__file__)
            system_prompt_file_path = os.path.join(base_dir, system_prompt_file_path)
            with open(system_prompt_file_path, "r") as f:
                self.system_prompt = f.read()

    def init_chat(self):
        chat = self.chat_model.start_chat(context=self.system_prompt)
        return chat

    def get_chat_response(self, chat: ChatSession, prompt: str, image=None):
        try:
            if image:
                image = Image(image)
                response = self.image_model.get_captions(image)[0]
                chat._message_history.extend(
                    [
                        ChatMessage(content="Given the image, what do you see", author="user"),
                        ChatMessage(content=f"I see: {response}", author="bot"),
                    ]
                )
                response = chat.send_message(prompt).text
            else:
                response = chat.send_message(prompt).text
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            response = "sorry, an error occured."
        return response
    
    def save_history(self, chat_id, chat_session: ChatSession):
        history = chat_session.message_history
        model_name = "google-chat-bison"  # replace with your actual model name
        self.redis_client.save_chat_session(chat_id, history, model_name)

    def get_history(self, chat_id):
        chat_session = self.init_chat()
        history = self.redis_client.get_chat_session(chat_id)
        if history is False:
            self.save_history(chat_id, chat_session)
        else:
            chat_session._message_history = history
        return chat_session
