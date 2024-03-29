from vertexai.language_models import ChatModel
from .agent import Agent
from ...ai_agents import functions
from ...language_models.google.setup import initialize_vertexai
import json
from ...prompts.prompt import AI_AGENTS
from ...redis.redis_client import RedisClient
import pickle

INSTRUCTION = AI_AGENTS["AGENT_1"]


class ChatBisonAgent(Agent):
    def __init__(self):
        initialize_vertexai()
        self.model = ChatModel.from_pretrained("chat-bison@001")
        self.redis_client = RedisClient()
        self.functions = {
            "get_time": functions.get_time,
            "generate_images": functions.generate_images,
            "search": functions.search,
        }
        self.INSTRUCTION = AI_AGENTS["AGENT_1"]

    def step(self, prompt, chat_id=None):
        function = self.get_function(prompt, chat_id)
        response = self.call_function(function)
        return response

    def get_function(self, prompt, chat_id=None):
        if chat_id:
            chat = self.get_agent_history(chat_id)
            response = chat.send_message(prompt)
            self.save_agent_history(chat_id, chat)
        else:
            chat = self.model.start_chat(context=self.INSTRUCTION)
            response = chat.send_message(prompt)
        print(response.text)
        return json.loads(response.text)

    def call_function(self, response):
        function_name = response.get("name")
        parameters = response.get("parameters")
        if function_name not in self.functions.keys():
            return "Function not found"
        function = self.functions[function_name]
        if parameters:
            return function(**parameters)
        else:
            return function()

    def respond(self, prompt, chat_id=None):
        return self.step(prompt, chat_id=chat_id)

    def save_agent_history(self, chat_id, chat_session):
        history = chat_session.message_history
        data = self.redis_client.get_data(chat_id)
        if data:
            data["agent_history"] = pickle.dumps(history)
            self.redis_client.save_data(chat_id, **data)
            print("Agent history saved")

    def get_agent_history(self, chat_id):
        chat = self.model.start_chat(context=INSTRUCTION)
        data = self.redis_client.get_data(chat_id)
        if data and data.get("agent_history"):
            history = pickle.loads(data["agent_history"])
            chat._message_history = history
            return chat
        self.save_agent_history(chat_id, chat)
        return chat
