import requests
from config.config import Config


def send_message(message, RECIPIENT_PHONE_NUMBER):
    try:
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": RECIPIENT_PHONE_NUMBER,
            "type": "text",
            "text": {
                "body": message,
                "preview_url": False,
            }
        }
        headers = {
            "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(Config.WHATSAPP_API_URL, json=payload, headers=headers)

        print(response.text)

        if response.status_code == 200:
            print("Message Sent")
        else:
            print(f"Error sending message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")

if __name__ == "__main__":
    message_to_send = "Hello, this is a test message from your WhatsApp bot!"
    send_message(message_to_send, "2348101667854")