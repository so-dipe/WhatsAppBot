import subprocess
from config.config import Config

def download_image(image_url, headers):
    url = Config.WHATSAPP_API_URL + image_url
    curl_command = f"""
        curl \
        '{url}' \
        -H 'Authorization: {headers["Authorization"]}' > media \
    """
    
    try:
        _ = subprocess.run(curl_command, shell=True, check=True, text=True)
        print("Image downloaded successfully.")
        with open("media", "rb") as f:
            image_bytes = f.read()
            print(image_bytes)
            return image_bytes
    except subprocess.CalledProcessError as e:
        print(f"Error downloading image: {e}")
