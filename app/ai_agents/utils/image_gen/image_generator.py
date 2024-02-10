from vertexai.preview.vision_models import ImageGenerationModel
from ....language_models.google.setup import initialize_vertexai

initialize_vertexai()

model = ImageGenerationModel.from_pretrained("imagegeneration@002")


def generate_images(prompt):
    """
    Generates images based on a prompt.

    Args:
        prompt (str): The prompt to generate images from.
        num_images (int): The number of images to generate.
        seed (int): The seed for the random number generator.

    Returns:
        list: The generated images.

    """
    try:
        response = model.generate_images(prompt)
        images = [image._image_bytes for image in response]
    except Exception as e:
        print(f"Error generating images: {str(e)}")
        return None
    return images[0]
