import torch
from PIL import Image

from app.model import get_model_loader
from app.preprocess import preprocess_image


def predict_image(image: Image.Image) -> dict:
    loader = get_model_loader()

    if not loader.is_ready():
        return {
            "label": None,
            "confidence": None,
            "probabilities": {},
            "error": "Model checkpoint not loaded yet. Add models/best_model.pth and models/class_names.json.",
        }

    input_tensor = preprocess_image(image).to(loader.device)

    with torch.no_grad():
        logits = loader.model(input_tensor)
        probabilities = torch.softmax(logits, dim=1).squeeze(0)

    confidence, predicted_index = torch.max(probabilities, dim=0)
    label = loader.class_names[predicted_index.item()]
    probability_map = {
        name: probabilities[index].item() for index, name in enumerate(loader.class_names)
    }

    return {
        "label": label,
        "confidence": confidence.item(),
        "probabilities": probability_map,
        "error": None,
    }
