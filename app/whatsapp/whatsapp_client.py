import requests
from config.config import Config
import json
import tempfile
import subprocess


class WhatsAppClient:
    """
    A client for interacting with the WhatsApp Business API.

    This class is responsible for processing payloads from the WhatsApp
    Business API as well as sending messages to the API.

    Attributes:
        headers (dict): The headers to be used for the API requests.
        API_URL (str): The base URL for the API.
        custom_messages (dict): A dictionary containing custom messages for
        the API.
        redis_client (RedisClient): An instance of the RedisClient class.

    Methods:
        send_message: Sends a text message to a recipient.
        send_template_message: Sends an interactive template message to a
        recipient.
        send_custom_message: Sends a custom message to a recipient.
        reply_message: Sends a reply to a message.
        process_payload: Processes a payload from the API.
        process_change: Processes a change in a payload.
        process_messages: Processes messages in a payload.
        process_model_selection: Processes a model selection message.
        process_personality_selection: Processes a personality selection
        message.
        process_interactive_message: Processes an interactive message.
        process_special_commands: Processes special commands in a message.
        send_welcome_message: Sends a welcome message to a recipient.
        send_select_model_message: Sends a message to select a model to a
        recipient.
        send_select_personality_message: Sends a message to select a
        personality to a recipient.
        upload_media: Uploads media to the API.
        upload_image: Uploads an image to the API.
        send_media: Sends media to a recipient.
        delete_media: Deletes a media from the API.
    """

    def __init__(self, redis_client):
        """
        Initializes the WhatsAppClient class.

        Parameters:
            redis_client (RedisClient): An instance of the RedisClient class.
        """
        self.headers = {
            "Authorization": f"Bearer {Config.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        self.API_URL = Config.WHATSAPP_API_URL + Config.NUMBER_ID
        with open("app/whatsapp/assets/messages.json", "r") as f:
            self.custom_messages = json.load(f)
        self.redis_client = redis_client

    def send_message(self, recipient_phone_number, message):
        """
        Sends a text message to a recipient.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
            message (str): The message to be sent.
        """
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
                },
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
        """
        Sends an interactive template message to a recipient.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
            template_name (str): The name of the template to be sent.
        """
        url = f"{self.API_URL}/messages/"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"policy": "deterministic", "code": "en"},
            },
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Error sending interactive template message: {str(e)}")

    def send_custom_message(self, recipient_phone_number, payload):
        """
        Sends a custom message to a recipient.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
            payload (dict): The payload to be sent.
        """
        try:
            url = f"{self.API_URL}/messages/"
            payload["to"] = recipient_phone_number
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Message sent successfully!")
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Error sending custom message: {str(e)}")

    def reply_message(self, recipient_phone_number, message_id, message):
        """
        Sends a reply to a message.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
            message_id (str): The ID of the message to be replied to.
            message (str): The reply message.
        """
        try:
            url = f"{self.API_URL}/messages/"
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient_phone_number,
                "context": {"message_id": message_id},
                "type": "text",
                "text": {
                    "body": message,
                    "preview_url": False,
                },
            }
            response = requests.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("Reply sent successfully!")
        except Exception as e:
            print(response.status_code)
            print(f"Error sending reply: {str(e)}")

    def process_payload(self, notification):
        """
        Processes a payload from the API.

        Parameters:
            notification (dict): The notification payload from the API.

        Returns:
            list: Processed messages extracted from payload.
        """
        try:
            processed_payloads = []
            entries = notification.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    processed_payload = self.process_change(change)
                    if processed_payload:
                        processed_payloads.extend(processed_payload)
            return processed_payloads
        except Exception as e:
            print(f"Error processing payload: {e}")

    def process_change(self, change):
        """
        Processes a change in a payload.

        Parameters:
            change (dict): The change to be processed.

        Returns:
            list: Processed messages extracted from change.
        """
        try:
            field = change.get("field", "")
            value = change.get("value", {})
            if field == "messages" and "messages" in value:
                messages = value["messages"]
                return self.process_messages(messages)
            elif field == "messages" and "statuses" in value:
                # TODO: Implement processing for statuses
                pass
        except Exception as e:
            print(f"Error processing change: {e}")

    def process_messages(self, messages):
        """
        Processes messages in a payload. Extracts relevant information from
        messages.
        Only processes text, image, audio, sticker, button, and interactive
        messages.

        Parameters:
            messages (list): The messages to be processed.

        Returns:
            list: The processed messages.
        """
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
                if processed_message["text"].startswith("/"):
                    processed_message["type"] = "command"
            elif message.get("type") in ["image", "audio", "sticker"]:
                media_type = message.get("type")
                media = message.get(media_type, {})
                processed_message["caption"] = media.get("caption")
                try:
                    url = f"{Config.WHATSAPP_API_URL}/{media.get('id')}"
                    response = requests.get(url=url, headers=self.headers)
                    url = response.json().get("url")
                    response = requests.get(url=url, headers=self.headers)
                    processed_message["media_bytes"] = response.content
                except Exception as e:
                    print(f"Error getting image URL: {e}")
            elif message.get("type") == "button":
                processed_message["text"] = message.get("button").get("text")
                processed_message["payload"] = message.get("button").get(
                    "payload"
                )
            elif message.get("type") == "interactive":
                processed_message["text"] = (
                    message.get("interactive").get("button_reply").get("title")
                )
            processed_messages.append(processed_message)
        return processed_messages

    def process_model_selection(self, message):
        """
        Processes a model selection message.

        Parameters:
            message (dict): The message to be processed.

        Returns:
            str: The reply message.
        """
        if "GEMINI PRO" in message["text"].upper():
            reply = (
                "GEMINI PRO selected. \n"
                "Starting a chat session with GEMINI PRO."
            )
        elif "MISXTRAL" in message["text"].upper():
            reply = (
                "MISXTRAL selected. \n"
                "Starting a chat session with MISXTRAL."
            )
        return reply

    def process_personality_selection(self, message):
        """
        Processes a personality selection message and saves the selected
        personality to redis.

        Parameters:
            message (dict): The message to be processed.

        Returns:
            str: A reply message.
        """
        data = self.redis_client.get_data(message["from"])
        command = message["text"].replace("personality", "").replace(" ", "")
        if "MARVIN" in command.upper():
            personality = "MARVIN"
            reply = "Hello, Marvin here... What do you want? (sigh)"
        elif "KVRC" in command.upper():
            personality = "K-VRC"
            reply = "I'm K-VRC."
        elif "1145G" in command.upper():
            personality = "11-45-G"
            reply = "11-45-G reporting for duty."
        elif "ZIMABLUE" in command.upper():
            personality = "ZimaBlue"
            reply = "ZimaBlue here. Let's get on with it."
        elif command == "/":
            personality = None
            reply = self.send_custom_message(
                message["from"], self.custom_messages["personalities"]
            )
        else:
            personality = None
            reply = (
                "Oops! It seems like that personality hasn't been programmed"
                " into me yet. Let's stick with the ones I know for now."
            )
        self.redis_client.save_data(
            message["from"], data["history"], data["model_name"], personality
        )
        return reply

    def process_interactive_message(self, message):
        """
        Processes an interactive message.

        Parameters:
            message (dict): The message to be processed.

        Returns:
            str: A reply message.
        """
        if message["text"] in ["GEMINI PRO", "MISXTRAL"]:
            reply = self.process_model_selection(message)
        elif message["text"] in ["MARVIN", "TARS", "JARVIS"]:
            reply = self.process_personality_selection(message)
        else:
            reply = (
                "I dont know how you got here, but I can't let you through."
            )
        return reply

    def process_special_commands(self, message):
        """
        Processes special commands in a message.

        Parameters:
            message (dict): The message to be processed.

        Returns:
            str: A reply message.
        """
        if "personality" in message["text"].lower():
            reply = self.process_personality_selection(message)
        elif "model" in message["text"].lower():
            reply = self.process_model_selection(message)
        elif "help" in message["text"].lower():
            pass
        elif "reset" in message["text"].lower():
            self.redis_client.delete_data(message["from"])
            print(f"Chat session for {message['from']} deleted.")
            reply = "Starting fresh, are we? What shall we do next?"
        else:
            reply = (
                "Oops! Looks like I'm not familiar with that command."
                "Let's try something else."
            )
        return reply

    def send_welcome_message(self, recipient_phone_number):
        """
        Sends a welcome message to a recipient. Message is defined in
        `self.custom_messages` and retrieved from messages.json.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
        """
        self.send_custom_message(
            recipient_phone_number, self.custom_messages["welcome_message"]
        )

    def send_select_model_message(self, recipient_phone_number):
        """
        Sends a message to select a model to a recipient. Message is defined
        in `self.custom_messages` and retrieved from messages.json.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
        """
        self.send_custom_message(
            recipient_phone_number, self.custom_messages["model_select"]
        )

    def send_select_personality_message(self, recipient_phone_number):
        """
        Sends a message to select a personality to a recipient. Message is
        defined in `self.custom_messages` and retrieved from messages.json.

        Parameters:
            recipient_phone_number (str): The phone number of the recipient.
        """
        self.send_custom_message(
            recipient_phone_number, self.custom_messages["personality_select"]
        )

    def upload_media(self, file_path, mime_type):
        """
        Uploads media to the API.

        Args:
            file_path (str): The path to the file to be uploaded.
            mime_type (str): The MIME type of the file.

        Returns:
            str: The ID of the uploaded media.
        """
        command = [
            "curl",
            "-X",
            "POST",
            f"{self.API_URL}/media",
            "-H",
            f'Authorization: {self.headers["Authorization"]}',
            "-F",
            f"file=@{file_path}",
            "-F",
            f"type={mime_type}",
            "-F",
            "messaging_product=whatsapp",
        ]
        try:
            response = subprocess.run(command, check=True, capture_output=True)
            response_data = json.loads(response.stdout.decode())
            if response.returncode == 0:
                media_id = response_data.get("id")
                return media_id
            else:
                print(response.returncode, response.stderr.decode())
        except Exception as e:
            print(f"Error uploading media: {str(e)}")

    def upload_image(self, image: bytes):
        """
        Uploads an image to the API.

        Args:
            image (bytes): The image to be uploaded.

        Returns:
            str: The ID of the uploaded image.
        """
        if len(image) > 1024 * 1024 * 5:
            print("Image size should not exceed 5MB")
            raise ValueError("Image size should not exceed 5MB")
        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            temp.write(image)
            temp.flush()

            media_id = self.upload_media(temp.name, mime_type="image/png")

        return media_id

    def send_media(
        self,
        recipient_phone_number,
        media_id,
        media_type,
        caption=None,
        filename=None,
    ):
        """
        Sends media to a recipient.

        Args:
            recipient_phone_number (str): The phone number of the recipient.
            media_id (str): The ID of the media to be sent.
            media_type (str): The type of media to be sent (Image, Audio, Doc,
            etc.)
            caption (str, optional): The caption for the media. Defaults to
            None.
            filename (str, optional): The filename of the media
            (Required for documents). Defaults to None.
        """
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_phone_number,
            "type": media_type,
            media_type: {
                "id": media_id,
            },
        }
        if caption:
            payload[media_type]["caption"] = caption
        if filename:
            payload[media_type]["filename"] = filename
        try:
            response = requests.post(
                f"{self.API_URL}/messages", json=payload, headers=self.headers
            )
            if response.status_code == 200:
                print("Image sent successfully!")
                self.delete_media(media_id)
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Error sending media: {str(e)}")

    def delete_media(self, media_id):
        """
        Deletes a media from the API.

        Args:
            media_id (str): The ID of the media to be deleted.
        """
        url = Config.WHATSAPP_API_URL + media_id

        try:
            response = requests.delete(url, headers=self.headers)
            if response.status_code == 200:
                print("Media deleted successfully!")
            else:
                print(response.status_code, response.text)
        except Exception as e:
            print(f"Error deleting media: {str(e)}")
