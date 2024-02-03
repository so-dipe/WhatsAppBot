import redis
from config.config import Config
import pickle


class RedisClient:
    def __init__(self) -> None:
        self.redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

    def save_data(self, chat_id, history, model_name, personality=None):
        try:
            if personality is None:
                personality = self.get_data(chat_id)["personality"]
            data = {
                "history": history,
                "model_name": model_name,
                "personality": personality,
            }
            data = pickle.dumps(data)
            with self.redis_client.pipeline() as pipe:
                pipe.set(chat_id, data)
                pipe.expire(chat_id, Config.REDIS_SESSION_LENGTH)
                pipe.execute()
        except Exception as e:
            print(f"Error saving chat session: {str(e)}")

    def get_data(self, chat_id):
        try:
            data = self.redis_client.get(chat_id)
            if data:
                data = pickle.loads(data)
                # print("data from redis", data, " for ", chat_id)
                return data
            else:
                return {
                    "history": False,
                    "model_name": None,
                    "personality": None,
                }
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None

    def get_model_name(self, chat_id):
        try:
            data = self.redis_client.get(chat_id)
            if data:
                data = pickle.loads(data)
                return data["model_name"]
            else:
                return None
        except Exception as e:
            print(f"Error getting model name: {str(e)}")
            return None

    def delete_data(self, chat_id):
        try:
            self.redis_client.delete(chat_id)
            print(f"Chat session for {chat_id} deleted.")
        except Exception as e:
            print(f"Error deleting chat session: {str(e)}")
            return None
