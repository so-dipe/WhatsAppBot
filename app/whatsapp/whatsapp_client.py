import requests
from config.config import Config
import json
import os

class WhatsAppClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        self.API_URL = Config.WHATSAPP_API_URL + Config.NUMBER_ID

    def send_message(self, recipient_phone_number, message):
        try:
            url = f"{self.API_URL}/messages/"
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "text",
                "text": {
                    "body": message,
                    "preview_url": False,
                }
            }
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(response.text)
                print("Failed to send message.")
        except Exception as e:
            print(f"Error sending message: {str(e)}")


    def send_template_message(self, recipient_phone_number, template_name):
        url = f"{self.API_URL}/messages/"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "policy": "deterministic",
                    "code": "en"
                }
            }
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Error sending interactive template message: {str(e)}")


    def reply_message(self, recipient_phone_number, message_id, message):
        try:
            url = f"{self.API_URL}/messages/"
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "context": {
                    "message_id": message_id
                },
                "type": "text",
                "text": {
                    "body": message,
                    "preview_url": False,
                }
            }
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Reply sent successfully!")
        except Exception as e:
            print(response.status_code)
            print(f"Error sending reply: {str(e)}")

    def process_payload(self, notification):
        try:
            processed_payloads = []
            entries = notification.get('entry', [])
            for entry in entries:
                changes = entry.get('changes', [])
                for change in changes:
                    processed_payload = self.process_change(change)
                    if processed_payload:
                        processed_payloads.extend(processed_payload)
            return processed_payloads
        except Exception as e:
            print(f"Error processing payload: {e}")

    def process_change(self, change):
        try:
            field = change.get('field', '')
            value = change.get('value', {})
            if field == 'messages' and 'messages' in value:
                messages = value['messages']
                return self.process_messages(messages)
            elif field == 'messages' and 'statuses' in value:
                #TODO: Implement processing for statuses
                pass
        except Exception as e:
            print(f"Error processing change: {e}")
    

    def process_messages(self, messages):
        processed_messages = []
        for message in messages:
            processed_message = {
                "from": message.get("from"),
                "id": message.get("id"),
                "timestamp": message.get("timestamp"),
                "type": message.get("type"),
            }
            if message.get("type") == "text":
                processed_message["text"] = message.get("text", {}).get("body")
            elif message.get("type") in ["image", "audio", "sticker"]:
                media_type = message.get("type")
                media = message.get(media_type, {})
                processed_message["caption"] = media.get("caption")
                try:
                    url = f"{Config.WHATSAPP_API_URL}/{media.get('id')}"
                    response = requests.get(url=url, headers=self.headers)
                    url = response.json().get('url')
                    response = requests.get(url=url, headers=self.headers)
                    processed_message["media_bytes"] = response.content
                except Exception as e:
                    print(f"Error getting image URL: {e}")
            elif message.get("type") == "button":
                processed_message['text'] = message.get('button').get('text')
                processed_message['payload'] = message.get('button').get('payload')
            processed_messages.append(processed_message)
        return processed_messages