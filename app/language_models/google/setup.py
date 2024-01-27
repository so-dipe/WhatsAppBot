import vertexai
import json
from google.oauth2 import service_account
from google.cloud import speech
from config.config import Config
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
SERVICE_ACCOUNT_PATH = os.path.abspath(os.path.join(CURRENT_PATH, "../../..", Config.SERVICE_ACCOUNT_PATH))

def initialize_vertexai():
    with open(SERVICE_ACCOUNT_PATH, "r") as f:
        credentials = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(credentials)

    vertexai.init(project=Config.GOOGLE_PROJECT_ID, credentials=credentials)
    speechclient = speech.SpeechClient(credentials=credentials)

def initialize_speech_client():
    with open(SERVICE_ACCOUNT_PATH, "r") as f:
        credentials = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(credentials)

    speechclient = speech.SpeechClient(credentials=credentials)
    return speechclient
