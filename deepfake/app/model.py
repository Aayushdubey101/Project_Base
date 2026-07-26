import json
from pathlib import Path
from threading import Lock

import torch
from torch import nn
from torchvision.models import resnet18

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
CHECKPOINT_PATH = MODELS_DIR / "best_model.pth"
CLASS_NAMES_PATH = MODELS_DIR / "class_names.json"


class ModelLoader:
    _instance = None
    _lock = Lock()

    def __new__(cls) -> "ModelLoader":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.class_names: list[str] = []
        self._load()
        self._initialized = True

    def _load(self) -> None:
        if CLASS_NAMES_PATH.exists():
            self.class_names = json.loads(CLASS_NAMES_PATH.read_text())
        if not CHECKPOINT_PATH.exists() or not self.class_names:
            return

        model = resnet18(weights=None)
        model.fc = nn.Linear(model.fc.in_features, len(self.class_names))
        checkpoint = torch.load(CHECKPOINT_PATH, map_location=self.device)
        model.load_state_dict(checkpoint["model_state_dict"])
        model.to(self.device)
        model.eval()
        self.model = model

    def is_ready(self) -> bool:
        return self.model is not None


def get_model_loader() -> ModelLoader:
    return ModelLoader()
