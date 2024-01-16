import requests
from config.config import Config

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
                print("Failed to send message.")
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def send_template_message(self, recipient_phone_number, template_name, template_parameters):
        try:
            url = f"{self.API_URL}/messages/"
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "type": "template",
                "template": {
                    "namespace": "your-namespace",
                    "name": template_name,
                    "language": {
                        "policy": "deterministic",
                        "code": "en"
                    },
                }
            }
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Template message sent successfully!")
            else:
                print("Failed to send template message.")
        except Exception as e:
            print(f"Error sending template message: {str(e)}")

    def process_notification(self, data):
        entries = data['entry']
        all_messages = []
        for entry in entries:
            for change in entry['changes']:
                if change['field'] == 'messages':
                    messages = change['value']['messages']
                    for message in messages:
                        if message['type'] == "text":
                            message_dict = {
                                "sender_no": message['from'],
                                "message": message['text']['body'],
                                "message_id": message['id'],

                            }
                            all_messages.append(message_dict)
        return all_messages