from vertexai.preview.generative_models import Part, Content, Image

class CustomPart:
    def __init__(self, text=None, inline_data=None):
        self.text = text
        self.inline_data = inline_data
        self._raw_part = Part.from_text(text=text)._raw_part
    
    @staticmethod
    def from_text(text):
        print(Part(text=text)._raw_part)
        return Part(text=text)
    @staticmethod
    def from_image(image):
        return Part(inline_data=image)
    @staticmethod
    def from_part(part: Part):
        print("converting part")
        return CustomPart(text=part.text)
    
    def __json__(self):
        return {
            "text": self.text,
            "inline_data": " "
        }

class CustomContent:
    def __init__(self, role: str = None, parts: [] = None):
        self.role = role
        self.parts = parts
        self._raw_content = Content(role=role, parts=parts)._raw_content
        # return super().__init__(role=role, parts=parts)
    
    @staticmethod
    def from_content(content: Content):
        print("converting content")
        parts = [CustomPart.from_part(part) for part in content.parts]
        return CustomContent(role=content.role, parts=parts)
    
    def __json__(self):
        dic = {
            "role": self.role,
            "parts": [part.__json__() for part in self.parts]
        }
        return dic

class ChatSession:
    def __init__(self, model):
        self.model = model
        self.history = []
        self.total_tokens = 0

    def send_message(self, prompt: str, image: Image = None) -> Content:
        if image:
            image_part = CustomPart.from_image(image)
            text_part = CustomPart.from_text(prompt)
            content = CustomContent(role='user', parts=[image_part, text_part])
            response = self.model.generate_content(content)
        else:
            text_part = Part.from_text(prompt)
            content = CustomContent(role='user', parts=[text_part])
            response = self.model.generate_content(content)
        response_content = response.candidates[0].content
        print(content)
        response_content = CustomContent.from_content(response_content)
        self.history.append(response_content)
        return response.text