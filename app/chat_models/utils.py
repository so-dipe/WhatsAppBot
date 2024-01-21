from vertexai.preview.generative_models import Part, Content, Image
import json 

def convert_history_to_dict(history):
    contents = []
    for content in history:
        parts = []
        for part in content.parts:
            if part.inline_data:
                print("dont save image")
            if hasattr(part, "text"):
                parts.append({
                    "text": part.text
                })
        contents.append(
            {
                "role": content.role,
                "parts": parts
            }
        )
    return json.dumps(contents)

def convert_dict_to_history(contents):
    contents = json.loads(contents)
    history = []
    for content in contents:
        parts = []
        for part in content['parts']:
            parts.append(
                Part.from_text(text=part['text'])
            )
        history.append(
            Content(role=content['role'], parts=parts)
        )
    return history