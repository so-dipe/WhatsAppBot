import redis
from config.config import Config
import pickle

class RedisClient:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)
    
    def save_chat_session(self, chat_id, history):
        try:
            history = pickle.dumps(history)
            with self.redis_client.pipeline() as pipe:
                pipe.set(chat_id, history)
                pipe.expire(chat_id, 60 * 5)
                pipe.execute()
        except Exception as e:
            print(f"Error saving chat session: {str(e)}")
    
    def get_chat_session(self, chat_id):
        try:
            history = self.redis_client.get(chat_id)
            if history:
                history = pickle.loads(history)
                return history
            else:
                return False
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None