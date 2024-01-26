import redis
from config.config import Config
import pickle

class RedisClient:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

    def save_data(self, chat_id, history, model_name):
        try:
            data = {'history': history, 'model_name': model_name}
            data = pickle.dumps(data)
            with self.redis_client.pipeline() as pipe:
                pipe.set(chat_id, data)
                pipe.expire(chat_id, 60 * 1)
                pipe.execute()
        except Exception as e:
            print(f"Error saving chat session: {str(e)}")

    def get_data(self, chat_id):
        try:
            data = self.redis_client.get(chat_id)
            if data:
                return pickle.loads(data)
            else:
                return {"history": False, "model_name": None}
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None

    def get_chat_session(self, chat_id):
        try:
            data = self.redis_client.get(chat_id)
            if data:
                data = pickle.loads(data)
                return data['history']
            else:
                return False
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None
        
    def get_model_name(self, chat_id):
        try:
            data = self.redis_client.get(chat_id)
            if data:
                data = pickle.loads(data)
                return data['model_name']
            else:
                return None
        except Exception as e:
            print(f"Error getting model name: {str(e)}")
            return None
        
    def delete_data(self, chat_id):
        try:
            self.redis_client.delete(chat_id)
        except Exception as e:
            print(f"Error deleting chat session: {str(e)}")
            return None