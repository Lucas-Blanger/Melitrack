from app.inference.anomaly.detector import AnomalyDetector
from app.inference.population.estimator import PopulationEstimator


class HiveAnalysisPipeline:
    def __init__(self):
        print("[Pipeline] loading models...")
        self.anomaly = AnomalyDetector()
        self.population = PopulationEstimator()
        print("[Pipeline] models ready")

    def run(self, image_bytes: bytes) -> dict:
        return {
            "anomaly": self.anomaly.predict(image_bytes),
            "population": self.population.predict(image_bytes),
        }


pipeline = HiveAnalysisPipeline()
