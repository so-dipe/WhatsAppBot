"""
This module defines special functions for the AI agents.
They are used to handle special requests that ChatModel cannot handle
accurately.
"""

from datetime import datetime
from .utils.image_gen import image_gen


def get_time():
    """
    A function to get the current time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_images(prompt, number_of_images=1, seed=42):
    """
    A function to generate images based on a prompt.
    """
    return image_gen.generate_images(prompt, number_of_images, seed)
