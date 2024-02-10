"""
This module initializes the Vertex AI client.
This is required to use the vertex ai generative models.

The initialize_vertexai function initializes the Vertex AI client with the
project id and service account credentials.

Project ID is stores as an environment variable in the .env file and retrieved
by Config.GOOGLE_PROJECT_ID. when the service account credentials are loaded
from file with the file path stored in the .env file and retrieved by
Config.SERVICE_ACCOUNT_PATH.

The initialize_vertexai function is called in the __init__ method of the
GeminiChatModel class in the gemini.py module as well as in the __init__ method
of the GoogleChatModel class in the google_chat_model.py module.
"""

import vertexai
import json
from google.oauth2 import service_account
from config.config import Config
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_PATH = os.path.abspath(
    os.path.join(CURRENT_PATH, "../../..", Config.SERVICE_ACCOUNT_PATH)
)


def initialize_vertexai():
    """
    Initialize the Vertex AI client with the project id and service account
    credentials.

    This function changes the state of the gemini and google_chat_model modules
    by initializing the Vertex AI client with the project id and service
    account credentials. After calling this function, the module will be able
    to use the Vertex AI generative models.
    """
    with open(SERVICE_ACCOUNT_PATH, "r") as f:
        credentials = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(
            credentials
        )
    vertexai.init(
        project=Config.GOOGLE_PROJECT_ID,
        credentials=credentials,
        location="us-central1",
    )
