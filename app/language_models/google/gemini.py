from vertexai.preview.generative_models import (
    GenerativeModel,
    Image,
    ChatSession,
    GenerationConfig,
    HarmCategory,
    HarmBlockThreshold,
    ResponseBlockedError,
)
from ...redis.redis_client import RedisClient
from .setup import initialize_vertexai
from ..chat_model import ChatModel, PERSONALITIES
import os


class GeminiChatModel(ChatModel):
    """
    A chat model for the Gemini Pro Vision model.
    This class is a subclass of the ChatModel class.

    Attributes:
    - model_name: The name of the chat model
    - redis_client: The redis client
    - model: The chat model
    - system_prompt: The system prompt
    - PERSONALITIES: different personalities for the chat model, retrieved from
    /assets/personalities.json
    - config: The generation config
    - safety_settings: The safety settings for the chat model

    Methods:
    - init_chat: Initialize the chat session
    - handle_image: Handle an image message
    - handle_audio: Handle an audio message
    - handle_text: Handle a text message
    - get_chat_response: Get a response from the chat model
    - save_history: Save the chat history
    - get_history: Get the chat history
    - save_chat_data: Save the chat data
    - get_chat_data: Get the chat data
    """

    def __init__(
        self,
        model_name="gemini-pro-vision",
        system_prompt_file_path="assets/gemini-prompt.txt",
    ):
        """
        Initialize the chat model.

        Parameters:
        - model_name: The name of the chat model, "gemini-pro-vision" by
        default, could also be "gemini-pro"
        - system_prompt_file_path: The system prompt file path,
        "assets/gemini-prompt.txt"
        """
        initialize_vertexai()
        self.model_name = model_name
        self.redis_client = RedisClient()
        self.model = GenerativeModel(model_name)
        if system_prompt_file_path:
            base_dir = os.path.dirname(__file__)
            system_prompt_file_path = os.path.join(
                base_dir, system_prompt_file_path
            )
            with open(system_prompt_file_path, "r") as f:
                self.system_prompt = f.read()
        self.PERSONALITIES = PERSONALITIES
        self.config = GenerationConfig(
            temperature=0.9,
            max_output_tokens=100,
        )
        self.safety_settings = {
            # hate speech - block all
            HarmCategory(1): HarmBlockThreshold(4),
            # dangerous content - block none
            HarmCategory(2): HarmBlockThreshold(4),
            # harassment - block most
            HarmCategory(3): HarmBlockThreshold(4),
            # sexually explicit - block some
            HarmCategory(4): HarmBlockThreshold(4),
        }

    def init_chat(self):
        """
        Initialize the chat session.

        Returns:
        - chat (ChatSession): The chat session
        """
        chat = self.model.start_chat()
        return chat

    async def handle_image(self, chat: ChatSession, image: bytes) -> str:
        """
        Handle an image message.

        Parameters:
        - chat (ChatSession): The chat session
        - image (bytes): The image as bytes

        Returns:
        - response_text (str): The response text

        Exceptions:
        - ResponseBlockedError: If the response is blocked
        - Exception: If an error occurs
        """
        image = Image.from_bytes(image)
        try:
            response = await chat.send_message_async(image)
            response_text = response.text
        except ResponseBlockedError as e:
            print(f"Error generating response: {str(e)}")
            response_text = (
                "sorry, I've been modified to"
                " stay away from certain topics."
            )
        except Exception as e:
            print(f"Error sending image: {str(e)}")
            response_text = (
                "It seems my engineers are a dud."
                " I can't speak. Check back later."
            )
        return response_text

    async def handle_audio(self, chat: ChatSession, audio: bytes) -> str:
        """
        Handle an audio message.

        Parameters:
        - chat (ChatSession): The chat session
        - audio (bytes): The audio as bytes

        Returns:
        Not Implemented
        """
        pass

    async def handle_text(
        self, chat: ChatSession, text: str, personality: str = "MARVIN"
    ) -> str:
        """
        Handle a text message.

        Parameters:
        - chat (ChatSession): The chat session
        - text (str): The text message
        - personality (str): The personality of the chat model, "MARVIN" by
        default

        Returns:
        - response_text (str): The response text

        Exceptions:
        - ResponseBlockedError: If the response is blocked
        - Exception: If an error occurs
        """
        try:
            # text = self.PERSONALITIES[personality] + text
            text = self.PERSONALITIES.get(personality, "") + text
            response = await chat.send_message_async(
                text,
                generation_config=self.config,
                safety_settings=self.safety_settings,
            )
            response_text = response.text
        except ResponseBlockedError as e:
            print(f"Error generating response: {str(e)}")
            response_text = (
                "sorry, I've been modified to be"
                " stay away from certain topics."
            )
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            response_text = (
                "It seems my engineers are a dud."
                " I can't speak. Check back later."
            )
        return response_text

    async def get_async_chat_response(
        self,
        chat: ChatSession,
        prompt: str,
        image=None,
        audio=None,
        personality=None,
    ) -> str:
        """
        Get a response from the chat model. This method is asynchronous.

        Parameters:
        - chat (ChatSession): The chat session
        - prompt (str): The prompt message
        - image (bytes): The image as bytes (Optional)
        - audio (bytes): The audio as bytes (Optional)
        - personality (str): The personality of the chat model (Optional)

        Returns:
        - response_text (str): The response text

        Exceptions:
        - ResponseBlockedError: If the response is blocked
        - Exception: If an error occurs

        Example:
        ```
        chat_model = GeminiChatModel()
        chat = chat_model.init_chat()
        response = await chat_model.get_async_chat_response(
            chat, "Hello, how are you?"
        )
        print(response)
        ```

        """
        if image:
            return await self.handle_image(chat, image)
        elif audio:
            return await self.handle_audio(chat, audio)
        else:
            return await self.handle_text(
                chat, prompt, personality=personality
            )

    def get_chat_response():
        pass

    def save_history(self, chat_id, chat_session):
        pass

    def get_history(self, chat_id):
        pass

    def save_chat_data(self, chat_id, chat_session, personality=None):
        """
        Save the chat data to a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)
        - chat_session: The chat session
        - personality (optional): Current personality of the chat model
        """
        history = chat_session.history
        self.redis_client.save_data(
            chat_id, history, self.model_name, personality
        )

    def get_chat_data(self, chat_id):
        """
        Get the chat data from a redis store.

        Parameters:
        - chat_id: The id of the chat (usually the phone number)

        Returns:
        - chat_session: The chat session
        - personality: The personality of the chat model
        """
        chat_session = self.init_chat()
        data = self.redis_client.get_data(chat_id)
        personality = data.get("personality")
        history = data.get("history", False)
        model_name = data.get("model_name", None)
        if (history is False) or model_name != self.model_name:
            self.save_chat_data(chat_id, chat_session, personality)
        else:
            chat_session._history = history
        return chat_session, personality
