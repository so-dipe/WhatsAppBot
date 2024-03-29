"""
This module provides the main utility functions for handling incoming
and processing outgoing messages.

It contains functions for handling all tasks related to sending post requests
to the whatsapp webhook.
"""

import random
from datetime import datetime, timedelta
from .whatsapp.whatsapp_client import WhatsAppClient
from .redis.redis_client import RedisClient
from .language_models.google.google_chat_model import GoogleChatModel
from .language_models.google.gemini import GeminiChatModel
from .ai_agents.agents.gemini import GeminiAgent
from .prompts.prompt import SUCCESS_MESSAGES


whatsapp_client = WhatsAppClient(redis_client=RedisClient())
redis_client = RedisClient()
# agent = ChatBisonAgent()
agent = GeminiAgent()

chat_models = [
    GoogleChatModel(),
    GeminiChatModel(),
]


def is_message_old(message):
    """
    This function checks if a message is older than 5 minutes.

    Args:
        message (dict): The message to check.

    Returns:
        bool: True if the message is older than 5 minutes, False otherwise.
    """
    now = datetime.now()
    timestamp = datetime.fromtimestamp(int(message["timestamp"]))
    difference = now - timestamp
    return difference > timedelta(minutes=3)


def get_chat_model(message):
    """
    This function gets the chat model to use for sending a message/reply
    based on the user's preference.

    Args:
        message (dict): The message to check.

    Returns:
        ChatModel: The chat model to use for sending a message/reply.
                    (if no model is found, it defaults to gemini-pro-vision)
    """
    model_name = redis_client.get_model_name(message["from"])
    if model_name == "gemini-pro-vision":
        return chat_models[1]
    elif model_name == "chat-bison@001":
        return chat_models[0]
    else:
        return chat_models[1]


def get_context(message):
    """
    Retrieves a context for a message from an AI agent.

    Args:
        message (dict): The message to get context for.

    Returns:
        str: The context of the message.
    """
    contexts = agent.respond(message["text"], message["from"])
    if not contexts:
        return None
    if isinstance(contexts, str):
        return contexts
    if isinstance(contexts, bytes):
        media_id = whatsapp_client.upload_image(contexts)
        whatsapp_client.send_media(message["from"], media_id, "image")
        return random.choice(SUCCESS_MESSAGES)


async def process_text_message(
    chat_model, chat_session, message, personality=None
):
    """
    Get a reply to a text message from the chat model.

    Args:
        chat_model (ChatModel): The chat model to use.
        chat_session (dict): The chat session to use.
        message (dict): The message to get a reply for.
        personality (str): The personality to use for the chat.

    Returns:
        str: The reply to the message.
    """
    context = get_context(message)
    if context:
        text = f"{message['text']} \n AI_AGENT: {context}"
        if context in SUCCESS_MESSAGES:
            return None
    else:
        text = message["text"]
    reply = await chat_model.get_async_chat_response(
        chat_session, text, personality=personality
    )
    return reply


async def process_image_message(
    chat_model, chat_session, message, personality=None
):
    """
    Get a reply to an image message from the chat model.

    Args:
        chat_model (ChatModel): The chat model to use.
        chat_session (dict): The chat session to use.
        message (dict): The message to get a reply for.
        personality (str): The personality to use for the chat.

    Returns:
        str: The reply to the message.
    """
    if message["caption"] is None:
        message["caption"] = "Explain this image."
    reply = await chat_model.get_async_chat_response(
        chat_session, message["caption"], message["media_bytes"]
    )
    return reply


async def process_message_by_type(
    chat_model, chat_session, message, personality=None
):
    """
    Get a reply to a message based on its type.

    Args:
        chat_model (ChatModel): The chat model to use.
        chat_session (dict): The chat session to use.
        message (dict): The message to get a reply for.
        personality (str): The personality to use for the chat.

    Returns:
        str: The reply to the message.
    """
    if message["type"] == "image":
        reply = await process_image_message(
            chat_model, chat_session, message, personality
        )
    elif message["type"] == "text":
        reply = await process_text_message(
            chat_model, chat_session, message, personality
        )
    elif message["type"] == "audio":
        pass
    elif message["type"] == "button":
        reply = process_button_message(message)
    elif message["type"] == "interactive":
        reply = whatsapp_client.process_interactive_message(message)
    else:
        reply = None
    return reply


def process_message_without_model(message):
    """
    Get a reply to a message when no has been selected.

    Args:
        message (dict): The message to get a reply for.

    Returns:
        str: The reply to the message.
    """
    if message["type"] == "button":
        reply = process_button_message(message)
    else:
        reply = "Sorry, you need to select a model to chat with."
    return reply


async def process_incoming_message(message):
    """
    Get a reply to an incoming message.

    Args:
        message (dict): The incoming message.

    Returns:
        str: The reply to the message.
    """
    chat_model = get_chat_model(message)
    if chat_model:
        chat_session, personality = chat_model.get_chat_data(message["from"])
        reply = await process_message_by_type(
            chat_model, chat_session, message, personality
        )
        chat_model.save_chat_data(message["from"], chat_session, personality)
        if message["type"] == "command":
            reply = whatsapp_client.process_special_commands(message)
    else:
        reply = process_message_without_model(message)
    return reply


def process_button_message(message):
    """
    For processing and getting reply to a button message.

    Args:
        message (dict): The message to get a reply for.

    Returns:
        str: The reply to the message.
    """
    if message["text"] == "get-started (default)":
        _ = chat_models[0].get_history(message["from"])
        reply = "Starting chat with google chat bison"
        print("starting chat with google chat bison")
    elif message["text"] == "gemini-pro-vision (beta)":
        _ = chat_models[1].get_history(message["from"])
        reply = "Starting chat with gemini pro vision"
        print("starting chat with gemini pro vision")
    else:
        reply = "Sorry, I don't understand that command."
    return reply
