from io import BytesIO

from PIL import Image

from app.inference.species import SpeciesClassifier


def _image_bytes(color: tuple[int, int, int] = (180, 135, 45)) -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (16, 16), color=color).save(buffer, format="PNG")
    return buffer.getvalue()


def test_species_classifier_returns_prediction_and_alternatives():
    result = SpeciesClassifier().predict(_image_bytes())

    assert result["prediction"]["label"]
    assert 0 <= result["prediction"]["confidence"] <= 1
    assert len(result["alternatives"]) == 3
