import vertexai
import json
from google.oauth2 import service_account
from config.config import Config

def initialize_vertexai():
    with open(Config.SERVICE_ACCOUNT_PATH, "r") as f:
        credentials = json.load(f)
        credentials = service_account.Credentials.from_service_account_info(credentials)

    vertexai.init(project=Config.GOOGLE_PROJECT_ID, credentials=credentials)