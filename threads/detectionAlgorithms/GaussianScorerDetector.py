from threads.DetectionThread import DetectionThread
from river import anomaly
from config.config import WARMUP_PERIOD, THRESHOLD


class GaussianScorerDetector(DetectionThread):
    def __init__(self, queue, websocket=None, threshold=THRESHOLD, window_size=WARMUP_PERIOD):
        super().__init__(queue, websocket=websocket)

        self._threshold = threshold
        self._window_size = window_size

        self._approach = 'gaussian_scorer'
        self.__detectors = {
            'heart_rate': anomaly.GaussianScorer(grace_period=self._window_size),
            'systolic_blood_pressure': anomaly.GaussianScorer(grace_period=self._window_size),
            'diastolic_blood_pressure': anomaly.GaussianScorer(grace_period=self._window_size),
            'temperature': anomaly.GaussianScorer(grace_period=self._window_size),
            'respiratory_rate': anomaly.GaussianScorer(grace_period=self._window_size),
            'glucose': anomaly.GaussianScorer(grace_period=self._window_size),
            'oxygen_saturation': anomaly.GaussianScorer(grace_period=self._window_size)
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
