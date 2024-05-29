from river import anomaly

from threads.DetectionThread import DetectionThread
from config.config import WARMUP_PERIOD, THRESHOLD


class HalfSpaceTreesDetector(DetectionThread):
    def __init__(self, queue, websocket=None, threshold=THRESHOLD, window_size=WARMUP_PERIOD):
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

        self._threshold = threshold
        self._window_size = window_size
        self._approach = 'half_space_trees'
        self._detector = anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits)
        self._detectors = {
            'heart_rate': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'systolic_blood_pressure': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'diastolic_blood_pressure': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'temperature': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'respiratory_rate': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'glucose': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits),
            'oxygen_saturation': anomaly.HalfSpaceTrees(window_size=self._window_size, limits=limits)
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
