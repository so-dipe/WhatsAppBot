"""
This file contains the configuration for the application. It
is used as a central place to store all the environment variables
and other configuration settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    This class contains the configuration settings for the application.
    It stores the environment variables and other configuration settings.

    Attributes:
    - WHATSAPP_ACCESS_TOKEN: The access token for the whatsapp API
    - WHATSAPP_API_URL: The URL for the whatsapp API e.g
    https://graph.facebook.com/v18.0/
    - VERIFY_TOKEN: The verification token for the whatsapp webhook
    - NUMBER_ID: The number id for the number used to send messages to end
    users
    - SERVICE_ACCOUNT_PATH: The path to the service account credentials file
    - GOOGLE_PROJECT_ID: The project id for the google cloud project
    - REDIS_URL: The URL for the redis server e.g redis://localhost:6379/
    - HUGGINGFACE_MODEL_API_URL: The URL for the huggingface model API if
    you choose to use huggingface models instead
    - HUGGINGFACE_TOKEN: The token for the huggingface model API
    - REDIS_SESSION_LENGTH: The length of time to store chat sessions on
    redis in seconds
    """

    WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_API_URL = os.environ.get("WHATSAPP_API_URL")
    VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
    NUMBER_ID = os.environ.get("NUMBER_ID")
    SERVICE_ACCOUNT_PATH = os.environ.get("SERVICE_ACCOUNT_PATH")
    GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
    REDIS_URL = os.environ.get("REDIS_URL")
    HUGGINGFACE_MODEL_API_URL = os.environ.get("HUGGINGFACE_MODEL_API_URL")
    HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
    REDIS_SESSION_LENGTH = os.environ.get("REDIS_SESSION_LENGTH")
    GOOGLE_SEARCH_API_KEY = os.environ.get("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_URL = os.environ.get("GOOGLE_SEARCH_URL")
    GOOGLE_SEARCH_ENGINE_ID = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
