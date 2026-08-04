import os
import logging

import tensorflow as tf

from app.inference.anomaly.preprocessor import preprocess
from app.inference.anomaly.labels import LABELS, THRESHOLDS, DESCRIPTIONS

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "../weights/anomaly_detector.h5")
logger = logging.getLogger(__name__)


def _build_model() -> tf.keras.Model:
    base = tf.keras.applications.EfficientNetB0(
        include_top=False, weights="imagenet", input_shape=(224, 224, 3)
    )
    base.trainable = False
    inputs = tf.keras.Input(shape=(224, 224, 3))
    x = base(inputs, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(3, activation="sigmoid")(x)
    return tf.keras.Model(inputs, outputs, name="anomaly_detector")


class AnomalyDetector:
    def __init__(self):
        self.model = _build_model()
        if os.path.exists(WEIGHTS_PATH):
            self.model.load_weights(WEIGHTS_PATH)
        else:
            logger.warning(
                "[AnomalyDetector] weights not found; using ImageNet without fine-tuning"
            )

    def predict(self, image_bytes: bytes) -> dict:
        tensor = preprocess(image_bytes)
        scores = self.model.predict(tensor, verbose=0)[0]
        alerts, results = [], {}
        for i, label in enumerate(LABELS):
            score = float(scores[i])
            results[label] = round(score, 4)
            if score >= THRESHOLDS[label]:
                alerts.append(
                    {"label": label, "description": DESCRIPTIONS[label], "score": score}
                )
        return {"scores": results, "alerts": alerts, "has_anomaly": len(alerts) > 0}
