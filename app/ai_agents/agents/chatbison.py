from vertexai.language_models import ChatModel
from .agent import Agent
from ...ai_agents import functions
from ...language_models.google.setup import initialize_vertexai
import json

with open("app/ai_agents/agents/instruct.txt", "r") as f:
    instruct = f.read()


class ChatBisonAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        initialize_vertexai()
        self.model = ChatModel.from_pretrained("chat-bison@001")
        self.functions = {
            "get_time": functions.get_time,
            "generate_images": functions.generate_images,
        }

    def get_functions(self, prompt):
        chat = self.model.start_chat(context=instruct)
        response = chat.send_message(prompt)
        print(response.text)
        return response.text

    def parse(self, prompt):
        results = []
        functions = self.get_functions(prompt)
        functions = json.loads(functions)
        for function in functions:
            function_name = function["name"]
            if function_name in self.functions.keys():
                if function["parameters"]:
                    results.append(
                        self.functions[function_name](**function["parameters"])
                    )
                else:
                    results.append(self.functions[function_name]())
        return results

    def respond(self, prompt):
        return self.parse(prompt)
