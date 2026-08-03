from io import BytesIO

import numpy as np
from PIL import Image

from app.inference.anomaly.preprocessor import preprocess as preprocess_anomaly
from app.inference.population.preprocessor import preprocess as preprocess_population


def _grayscale_image_bytes() -> bytes:
    buffer = BytesIO()
    Image.new("L", (32, 16), color=180).save(buffer, format="PNG")
    return buffer.getvalue()


def test_anomaly_preprocessor_outputs_efficientnet_input_shape():
    tensor = preprocess_anomaly(_grayscale_image_bytes())

    assert tensor.shape == (1, 224, 224, 3)
    assert tensor.dtype == np.float32


def test_population_preprocessor_outputs_efficientnet_input_shape():
    tensor = preprocess_population(_grayscale_image_bytes())

    assert tensor.shape == (1, 224, 224, 3)
    assert tensor.dtype == np.float32
