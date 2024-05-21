from threads.DetectionThread import DetectionThread
from river import anomaly
from config.warmup import WARMUP_PERIOD


class GaussianScorerDetector(DetectionThread):
    def __init__(self, queue, websocket=None):
        super().__init__(queue, websocket=websocket)

        self.__detectors = {
            'heart_rate': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'systolic_blood_pressure': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'diastolic_blood_pressure': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'temperature': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'respiratory_rate': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'glucose': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD),
            'oxygen_saturation': anomaly.GaussianScorer(grace_period=WARMUP_PERIOD)
        }

    def learn_one(self, processing_tuple_dict):
        for key in processing_tuple_dict:
            if key in self.__detectors:
                self.__detectors[key].learn_one(None, processing_tuple_dict[key])

    def score_one(self, processing_tuple_dict):
        scores = {}
        for key in processing_tuple_dict:
            if key in self.__detectors:
                scores[key] = self.__detectors[key].score_one(None, processing_tuple_dict[key])

        return scores
