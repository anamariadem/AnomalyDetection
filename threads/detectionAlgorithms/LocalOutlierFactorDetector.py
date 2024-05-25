from threads.DetectionThread import DetectionThread
from river import anomaly
from config.config import WARMUP_PERIOD


class LocalOutlierFactorDetector(DetectionThread):
    def __init__(self, queue, websocket=None):
        super().__init__(queue, websocket=websocket)

        self._threshold = 1.2
        self._approach = 'local_outlier_factor'
        self.__detectors = {
            'heart_rate': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'systolic_blood_pressure': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'diastolic_blood_pressure': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'temperature': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'respiratory_rate': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'glucose': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD),
            'oxygen_saturation': anomaly.LocalOutlierFactor(n_neighbors=WARMUP_PERIOD)
        }

    def learn_one(self, processing_tuple_dict):
        for key in processing_tuple_dict:
            if key in self.__detectors:
                self.__detectors[key].learn_one({key: processing_tuple_dict[key]})

    def score_one(self, processing_tuple_dict):
        scores = {}
        for key in processing_tuple_dict:
            if key in self.__detectors:
                scores[key] = self.__detectors[key].score_one({key: processing_tuple_dict[key]})

        return scores
