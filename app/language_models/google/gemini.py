from vertexai.preview.generative_models import GenerativeModel, Image, ChatSession
from ...redis.redis_client import RedisClient
from .setup import initialize_vertexai, initialize_speech_client
from ..chat_model import ChatModel
import os
from google.cloud import speech

speech_client = initialize_speech_client()

def transcribe(audio : bytes):
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
    def __init__(self, model_name="gemini-pro-vision", system_prompt_file_path="assets/gemini-prompt.txt"):
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

    def get_chat_response(self, chat: ChatSession, prompt: str, image=None, audio=None) -> str:
        if image:
            image = Image.from_bytes(image)
            try:
                response = chat.send_message([prompt, image]).text
            except Exception as e:
                print(f"Error sending image: {str(e)}")
                response = "Couldn't generate a response."
        elif audio:
            try:
                text = transcribe(audio)
                response = chat.send_message(text).text
            except Exception as e:
                print(f"Error sending audio: {str(e)}")
                response = "Couldn't generate a response."
        else:
            prompt = f"<SYS> Context: {self.system_prompt} <SYS> \n Query: {prompt}"
            try:
                response = chat.send_message(prompt).text
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                response = "Couldn't generate a response."
        return response

    async def get_async_chat_response(self, chat: ChatSession, prompt: str, image=None, audio=None) -> str:
        if image:
            image = Image.from_bytes(image)
            try:
                response = await chat.send_message_async([prompt, image])
                response = response.text
            except Exception as e:
                print(f"Error sending image: {str(e)}")
                response = "Couldn't generate a response."
        elif audio:
            try:
                text = transcribe(audio)
                response = await chat.send_message_async(text)
                response = f"Transcript: {text} \n Response: {response.text}"
            except Exception as e:
                print(f"Error sending audio: {str(e)}")
                response = "Couldn't generate a response."
        else:
            prompt = f"{self.system_prompt} \n {prompt}"
            try:
                response = await chat.send_message_async(prompt)
                response = response.text
            except Exception as e:
                print(f"Error sending message: {str(e)}")
                response = "Couldn't generate a response."
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