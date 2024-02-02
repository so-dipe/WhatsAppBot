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
from .setup import initialize_vertexai, initialize_speech_client
from ..chat_model import ChatModel, PERSONALITIES
import os
from google.cloud import speech

speech_client = initialize_speech_client()


def transcribe(audio: bytes):
    print("audio type", type(audio))
    audio = speech.RecognitionAudio(content=audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = speech_client.recognize(config=config, audio=audio)
    for result in response.results:
        return format(result.alternatives[0].transcript)


class GeminiChatModel(ChatModel):
    def __init__(
        self,
        model_name="gemini-pro-vision",
        system_prompt_file_path="assets/gemini-prompt.txt",
    ):
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
            max_output_tokens=200,
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
        chat = self.model.start_chat()
        return chat

    async def handle_image(self, chat: ChatSession, image: bytes) -> str:
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
        pass

    async def handle_text(
        self, chat: ChatSession, text: str, personality: str = "MARVIN"
    ) -> str:
        try:
            text = self.PERSONALITIES[personality] + text
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
        self, chat: ChatSession, prompt: str, image=None, audio=None
    ) -> str:
        if image:
            return await self.handle_image(chat, image)
        elif audio:
            return await self.handle_audio(chat, audio)
        else:
            return await self.handle_text(chat, prompt)

    def get_chat_response():
        pass

    def save_history(self, chat_id, chat_session):
        history = chat_session.history
        model_name = "gemini-pro-vision"
        self.redis_client.save_data(chat_id, history, model_name)

    def get_history(self, chat_id):
        chat_session = self.init_chat()
        data = self.redis_client.get_data(chat_id)
        history = data["history"]
        if (history is False) or (data["model_name"] != self.model_name):
            self.save_history(chat_id, chat_session)
        else:
            chat_session._history = history
        return chat_session
