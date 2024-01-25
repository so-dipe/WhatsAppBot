from datetime import datetime, timedelta

def is_message_old(message):
    now = datetime.now()
    timestamp = datetime.fromtimestamp(int(message['timestamp']))
    difference = now - timestamp
    return difference > timedelta(minutes=5)

def get_chat_model(redis_client, message, chat_models):
    model_name = redis_client.get_model_name(message['from'])
    print(model_name)
    if model_name == "gemini-pro-vision":
        return chat_models[1]
    elif model_name == "google-chat-bison":
        return chat_models[0]
    else: 
        return chat_models[0]
    
def process_incoming_message(chat_model, chat_models, message):
    chat_session = chat_model.get_history(message['from'])
    if message['type'] == 'image':
        if message['caption'] is None:
            message['caption'] = "Explain this image."
        reply = chat_model.get_chat_response(chat_session, message['caption'], message['media_bytes'])
    elif message['type'] == 'text':        
        reply =  chat_model.get_chat_response(chat_session, message['text'])
    elif message['type'] == 'button':
        if message['text'] == "get-started (default)":
            chat_session = chat_models[0].get_history(message['from'])
            print("starting chat with google chat bison")
        elif message['text'] == "gemini-pro-vision (beta)":
            chat_session = chat_models[1].get_history(message['from'])
            print("starting chat with gemini pro vision")
    else:
        reply = "Sorry, I didn't understand that."
    return reply, chat_session
