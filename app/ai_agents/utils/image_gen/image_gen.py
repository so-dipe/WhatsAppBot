from vertexai.preview.vision_models import ImageGenerationModel
from ....language_models.google.setup import initialize_vertexai

initialize_vertexai()

model = ImageGenerationModel.from_pretrained("imagegeneration@002")


def generate_images(prompt, num_images=1, seed=42):
    response = model.generate_images(
        prompt, number_of_images=num_images, seed=seed
    )
    images = [image._image_bytes for image in response]
    return images
