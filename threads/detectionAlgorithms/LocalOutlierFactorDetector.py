from threads.DetectionThread import DetectionThread
from river import anomaly


class LocalOutlierFactorDetector(DetectionThread):
    def __init__(self, queue, websocket=None):
        super().__init__(queue, websocket=websocket)

        # todo set warmup period
        self.__detectors = {
            'heart_rate': anomaly.LocalOutlierFactor(n_neighbors=20),
            'systolic_blood_pressure': anomaly.LocalOutlierFactor(n_neighbors=20),
            'diastolic_blood_pressure': anomaly.LocalOutlierFactor(n_neighbors=20),
            'temperature': anomaly.LocalOutlierFactor(n_neighbors=20),
            'respiratory_rate': anomaly.LocalOutlierFactor(n_neighbors=20),
            'glucose': anomaly.LocalOutlierFactor(n_neighbors=20),
            'oxygen_saturation': anomaly.LocalOutlierFactor(n_neighbors=20)
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
