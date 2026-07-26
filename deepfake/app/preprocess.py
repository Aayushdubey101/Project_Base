from io import BytesIO

import numpy as np
import torch
from PIL import Image
from torchvision import transforms

IMAGE_SIZE = 224

image_transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)


def load_image(image_bytes: bytes) -> Image.Image:
    return Image.open(BytesIO(image_bytes)).convert("RGB")


def preprocess_image(image: Image.Image) -> torch.Tensor:
    tensor = image_transform(image)
    return tensor.unsqueeze(0)


def image_to_array(image: Image.Image) -> np.ndarray:
    return np.array(image)
