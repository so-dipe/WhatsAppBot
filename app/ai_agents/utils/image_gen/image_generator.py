from vertexai.preview.vision_models import ImageGenerationModel
from ....language_models.google.setup import initialize_vertexai

initialize_vertexai()

model = ImageGenerationModel.from_pretrained("imagegeneration@002")


def generate_images(prompt, num_images=1, seed=42):
    """
    Generates images based on a prompt.

    Args:
        prompt (str): The prompt to generate images from.
        num_images (int): The number of images to generate.
        seed (int): The seed for the random number generator.

    Returns:
        list: The generated images.

    """
    response = model.generate_images(prompt, number_of_images=1, seed=seed)
    images = [image._image_bytes for image in response]
    return images[0]