from vertexai.preview.generative_models import GenerativeModel
from .agent import Agent
from ...ai_agents import functions
from ...language_models.google.setup import initialize_vertexai
from ...prompts.prompt import AI_AGENTS
from ...redis.redis_client import RedisClient
import pickle
import json


class GeminiAgent(Agent):
    def __init__(self):
        initialize_vertexai()
        self.model = GenerativeModel("gemini-pro")
        self.redis_client = RedisClient()
        self.functions = {
            "get_time": functions.get_time,
            "generate_images": functions.generate_images,
            "search": functions.search,
            # "view_link": functions.view_link,
        }
        self.INSTRUCTION = AI_AGENTS["AGENT_2"]

    def get_function(self, prompt, chat_id):
        try:
            chat = self.get_agent_history(chat_id)
            response = chat.send_message(self.INSTRUCTION + str(prompt))
            self.save_agent_history(chat_id, chat)
            response = response.text.replace("```json", "").replace("```", "")
            return json.loads(response)
        except Exception as e:
            print(f"Error getting function: {str(e)}")

    def call_function(self, response):
        try:
            function_name = response.get("name")
            parameters = response.get("parameters")
        except Exception as e:
            print(f"Error getting function name or parameters: {str(e)}")
            return None
        if function_name not in self.functions.keys():
            return None
        function = self.functions[function_name]
        if parameters:
            return function(**parameters)
        else:
            return function()

    def step(self, prompt, chat_id=None):
        function = self.get_function(prompt, chat_id)
        response = self.call_function(function)
        # if response and not isinstance(response, bytes):
        #     self.step(response, chat_id)
        return response

    def respond(self, prompt, chat_id=None):
        return self.step(prompt, chat_id=chat_id)

    def save_agent_history(self, chat_id, chat_session):
        history = chat_session.history
        data = self.redis_client.get_data(chat_id)
        if data:
            data["agent_history"] = pickle.dumps(history)
            self.redis_client.save_data(chat_id, **data)

    def get_agent_history(self, chat_id):
        chat = self.model.start_chat()
        data = self.redis_client.get_data(chat_id)
        if data and data.get("agent_history"):
            history = pickle.loads(data["agent_history"])
            chat._history = history
            return chat
        self.save_agent_history(chat_id, chat)
        return chat
