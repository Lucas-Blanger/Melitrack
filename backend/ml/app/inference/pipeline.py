from app.inference.anomaly.detector import AnomalyDetector
from app.inference.population.estimator import PopulationEstimator


class HiveAnalysisPipeline:
    def __init__(self):
        print("[Pipeline] loading models...")
        self.anomaly = AnomalyDetector()
        self.population = PopulationEstimator()
        print("[Pipeline] models ready")

    def run(self, image_bytes: bytes) -> dict:
        print("[Pipeline] Running AnomalyDetector...")
        anomaly_res = self.anomaly.predict(image_bytes)
        print("[Pipeline] Running PopulationEstimator...")
        population_res = self.population.predict(image_bytes)
        return {
            "anomaly": anomaly_res,
            "population": population_res,
        }


_pipeline_instance = None


def get_pipeline() -> HiveAnalysisPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = HiveAnalysisPipeline()
    return _pipeline_instance

