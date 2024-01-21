import redis
import json
from vertexai.preview.generative_models import ChatSession
from ..chat_models.utils import convert_history_to_dict, convert_dict_to_history
from config.config import Config
from ..chat_models.gemini import model, init_chat

class RedisClient:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)
    
    def save_chat_session(self, chat_id, chat_session: ChatSession):
        try:
            chat_history = convert_history_to_dict(chat_session.history)
            with self.redis_client.pipeline() as pipe:
                pipe.set(chat_id, chat_history)
                pipe.expire(chat_id, 60 * 3)
                pipe.execute()
        except Exception as e:
            print(f"Error saving chat session: {str(e)}")
    
    def get_chat_session(self, chat_id):
        try:
            chat_history = self.redis_client.get(chat_id)
            if chat_history:
                chat_session = ChatSession(model)
                chat_session._history = convert_dict_to_history(chat_history)
                return chat_session
            else:
                return init_chat()
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None
