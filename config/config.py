import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_API_URL = os.environ.get("WHATSAPP_API_URL")
    NUMBER_ID = os.environ.get("NUMBER_ID")
    SERVICE_ACCOUNT_PATH = os.environ.get("SERVICE_ACCOUNT_PATH")
    GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
    REDIS_URL = os.environ.get("REDIS_URL")
