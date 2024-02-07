"""
This module defines special functions for the AI agents.
They are used to handle special requests that ChatModel cannot handle
accurately.
"""

from datetime import datetime
from .utils.image_gen import image_generator


def get_time():
    """
    A function to get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_images(prompt, number_of_images=1, seed=42):
    """
    A function to generate images based on a prompt.

    Args:
        prompt (str): The prompt to generate images from.
        number_of_images (int): The number of images to generate.
        seed (int): The seed for the random number generator.
    """
    return image_generator.generate_images(prompt, number_of_images, seed)
