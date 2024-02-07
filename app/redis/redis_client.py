import redis
from config.config import Config
import pickle


class RedisClient:
    """
    A class to represent a Redis client.
    This class is responsible for saving and retrieving chat data for each user

    Attributes:
        redis_client: the redis object to interact with the redis server

    Methods:
        save_data: Save chat data to the redis server
        get_data: Get chat data from the redis server
        get_model_name: Get the model name from the redis server
        delete_data: Delete chat data from the redis server

    """

    def __init__(self) -> None:
        """
        Initializes the redis client object
        """
        self.redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

    def save_data(
        self,
        chat_id,
        history,
        model_name,
        personality=None,
        agent_history=None,
    ):
        """
        Saves the chat data to the redis store.

        Parameters:
            chat_id: A unique identifier for the chat
            (usually the phone number of the user)
            history: the conversations that should be saved to the redis store
            model_name: the name of the model presently being used for the
            conversation. It is important to specify the model name because
            each model stores and handles history differently. For example,
            chat-bison and gemini-pro both use message_history and history in
            their respective chat session to store past messages
            personality: the currently personality selected by the user
            (Optional, defaults to None)
        """
        try:
            if personality is None:
                personality = self.get_data(chat_id)["personality"]
            if agent_history is None:
                agent_history = self.get_data(chat_id)["agent_history"]
            data = {
                "history": history,
                "model_name": model_name,
                "personality": personality,
                "agent_history": agent_history,
            }
            data = pickle.dumps(data)
            with self.redis_client.pipeline() as pipe:
                pipe.set(chat_id, data)
                pipe.expire(chat_id, Config.REDIS_SESSION_LENGTH)
                pipe.execute()
        except Exception as e:
            print(f"Error saving chat session: {str(e)}")

    def get_data(self, chat_id):
        """
        Gets data from redis store

        Parameters:
            chat_id: The unique identifer for the chat in redis store
            (usually the phone number of the user)

        Returns:
            data: The chat data from the redis store
        """
        try:
            data = self.redis_client.get(chat_id)
            if data:
                data = pickle.loads(data)
                return data
            else:
                return {
                    "history": False,
                    "model_name": None,
                    "personality": None,
                    "agent_history": None,
                }
        except Exception as e:
            print(f"Error getting chat session: {str(e)}")
            return None

    def get_model_name(self, chat_id):
        """
        Gets model name from redis store

        Parameters:
            chat_id: The unique identifer for the chat in redis store
            (usually the phone number of the user)

        Returns:
            model_name (str): The name of the model currently being used
        """
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
        """
        Deletes data from the redis store

        Parameters:
            chat_id: The unique identifer for the chat in redis store
            (usually the phone number of the user)
        """
        try:
            self.redis_client.delete(chat_id)
            print(f"Chat session for {chat_id} deleted.")
        except Exception as e:
            print(f"Error deleting chat session: {str(e)}")
            return None
