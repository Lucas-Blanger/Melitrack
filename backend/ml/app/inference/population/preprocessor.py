import numpy as np
from PIL import Image
import io

TARGET_SIZE = (224, 224)


def preprocess(image_bytes: bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize(TARGET_SIZE)
    array = np.array(image, dtype=np.float32)
    array = np.expand_dims(array, axis=0)
    return array
