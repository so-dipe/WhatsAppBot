"""
This module defines special functions for the AI agents.
They are used to handle special requests that ChatModel cannot handle
accurately.
"""

from datetime import datetime
from .utils.image_gen import image_generator
from .utils.web_search import google


def get_time():
    """
    A function to get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_images(prompt):
    """
    A function to generate images based on a prompt.

    Args:
        prompt (str): The prompt to generate images from.
        number_of_images (int): The number of images to generate.
        seed (int): The seed for the random number generator.
    """
    return image_generator.generate_images(prompt)


def search(query):
    """
    This function sends a post request to the google search webhook
    and returns the response.

    Args:
        query (str): The query to search for.

    Returns:
        dict: The response from the google search webhook.
    """
    return google.get_search_results(query)


def view_link(url):
    """
    Returns the contents of a url.

    Args:
        url (str): The url to view.

    Returns:
        dict: The response from the google search webhook.
    """
    return google.view_link(url)
