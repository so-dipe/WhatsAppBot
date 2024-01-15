import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_API_URL = os.environ.get("WHATSAPP_API_URL")
