import io
import json
from pathlib import Path

import numpy as np
from PIL import Image
from tensorflow import keras

from app.inference.species.labels import SPECIES

MODEL_DIR = Path(__file__).resolve().parent / "training" / "models" / "v1"
MODEL_PATH = MODEL_DIR / "species_model.keras"
LABELS_PATH = MODEL_DIR / "labels.json"

IMG_SIZE = (224, 224)

_SCIENTIFIC_NAME_BY_LABEL = {
    s["label"].casefold(): s["scientific_name"] for s in SPECIES
}
_SCIENTIFIC_NAME_BY_LABEL.update(
    {
        "jatai": "Tetragonisca angustula",
        "mandacaia": "Melipona quadrifasciata",
        "urucu": "Melipona scutellaris",
    }
)


class SpeciesClassifier:
    def __init__(self, model_path: Path = MODEL_PATH, labels_path: Path = LABELS_PATH):
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found in {model_path}. ")
        self._model = keras.models.load_model(model_path)

        with open(labels_path, "r", encoding="utf-8") as f:
            self._class_names: list[str] = json.load(f)

    def predict(self, image_bytes: bytes) -> dict:
        batch = self._preprocess(image_bytes)
        raw_scores = self._model.predict(batch, verbose=0)[0]

        predictions = []
        for label, score in zip(self._class_names, raw_scores):
            predictions.append(
                {
                    "label": label,
                    "scientific_name": _SCIENTIFIC_NAME_BY_LABEL.get(
                        label.casefold(), "unknown"
                    ),
                    "confidence": round(float(score), 4),
                }
            )

        predictions.sort(key=lambda item: item["confidence"], reverse=True)

        return {
            "prediction": predictions[0],
            "alternatives": predictions[1:4],
        }

    def _preprocess(self, image_bytes: bytes) -> np.ndarray:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(IMG_SIZE)
        array = np.asarray(image, dtype=np.float32)
        array = keras.applications.efficientnet.preprocess_input(array)
        return np.expand_dims(array, axis=0)


_classifier_instance: SpeciesClassifier | None = None


def get_classifier() -> SpeciesClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = SpeciesClassifier()
    return _classifier_instance
