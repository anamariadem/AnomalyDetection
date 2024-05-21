from river import anomaly

from threads.DetectionThread import DetectionThread
from config.warmup import WARMUP_PERIOD


class HalfSpaceTreesDetector(DetectionThread):
    def __init__(self, queue, websocket=None):
        super().__init__(queue, websocket=websocket)

        limits = {
            'heart_rate': (40, 160),
            'systolic_blood_pressure': (90, 150),
            'diastolic_blood_pressure': (60, 100),
            'temperature': (35, 41),
            'respiratory_rate': (12, 25),
            'glucose': (70, 130),
            'oxygen_saturation': (70, 100)
        }

        self._detector = anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits)
        self._detectors = {
            'heart_rate': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'systolic_blood_pressure': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'diastolic_blood_pressure': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'temperature': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'respiratory_rate': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'glucose': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits),
            'oxygen_saturation': anomaly.HalfSpaceTrees(window_size=WARMUP_PERIOD, limits=limits)
        }

    def learn_one(self, processing_tuple_dict):
        if self._detector is not None:
            self._detector.learn_one(processing_tuple_dict)

        for key in processing_tuple_dict:
            if key in self._detectors:
                self._detectors[key].learn_one({key: processing_tuple_dict[key]})

    def score_one(self, processing_tuple_dict):
        scores = {}
        if self._detector is not None:
            scores['all'] = self._detector.score_one(processing_tuple_dict)

        for key in processing_tuple_dict:
            if key in self._detectors:
                scores[key] = self._detectors[key].score_one({key: processing_tuple_dict[key]})

        return scores
