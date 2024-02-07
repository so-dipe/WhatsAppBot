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
    def __init__(self, name):
        super().__init__(name)
        initialize_vertexai()
        self.model = ChatModel.from_pretrained("chat-bison@001")
        self.redis_client = RedisClient()
        self.functions = {
            "get_time": functions.get_time,
            "generate_images": functions.generate_images,
        }

    def get_functions(self, prompt, chat_id=None):
        if chat_id:
            chat = self.get_agent_history(chat_id)
            print(chat.message_history)
            response = chat.send_message(prompt)
            self.save_agent_history(chat_id, chat)
        else:
            chat = self.model.start_chat(context=INSTRUCTION)
            response = chat.send_message(prompt)

        print(response.text)
        return response.text

    def parse(self, prompt, chat_id=None):
        results = []
        functions = self.get_functions(prompt, chat_id)
        functions = json.loads(functions)
        for function in functions:
            function_name = function["name"]
            if function_name in self.functions.keys():
                if function.get("parameters"):
                    results.append(
                        self.functions[function_name](**function["parameters"])
                    )
                else:
                    results.append(self.functions[function_name]())
        return results

    def respond(self, prompt, chat_id=None):
        return self.parse(prompt, chat_id)

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
