from models.InputTuple import InputTuple


class PatientVitalsTuple(InputTuple):
    def __init__(self, _id, timestamp, heart_rate, systolic_blood_pressure, diastolic_blood_pressure, temperature,
                 oxygen_saturation, respiratory_rate, glucose):
        super().__init__(_id)
        self.__timestamp = timestamp
        self.__heart_rate = heart_rate
        self.__systolic_blood_pressure = systolic_blood_pressure
        self.__diastolic_blood_pressure = diastolic_blood_pressure
        self.__temperature = temperature
        self.__oxygen_saturation = oxygen_saturation
        self.__respiratory_rate = respiratory_rate
        self.__glucose = glucose
        self.__anomaly_scores = {}

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def heart_rate(self):
        return self.__heart_rate

    @property
    def systolic_blood_pressure(self):
        return self.__systolic_blood_pressure

    @property
    def diastolic_blood_pressure(self):
        return self.__diastolic_blood_pressure

    @property
    def temperature(self):
        return self.__temperature

    @property
    def oxygen_saturation(self):
        return self.__oxygen_saturation

    @property
    def respiratory_rate(self):
        return self.__respiratory_rate

    @property
    def glucose(self):
        return self.__glucose

    @property
    def anomaly_scores(self):
        return self.__anomaly_scores

    def set_anomaly_score(self, anomaly_type, score):
        self.__anomaly_scores[anomaly_type] = score

    def set_anomaly_score_dict(self, anomaly_scores):
        self.__anomaly_scores = anomaly_scores

    def __str__(self):
        return "({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7})".format(self.__timestamp, self.__heart_rate,
                                                                 self.__systolic_blood_pressure,
                                                                 self.__diastolic_blood_pressure, self.__temperature,
                                                                 self.__oxygen_saturation, self.__respiratory_rate,
                                                                 self.__glucose)

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return iter(
            [self.__heart_rate, self.__systolic_blood_pressure, self.__diastolic_blood_pressure, self.__temperature,
             self.__oxygen_saturation, self.__respiratory_rate, self.__glucose])

    def to_dict(self):
        return {
            'heart_rate': self.__heart_rate,
            'systolic_blood_pressure': self.__systolic_blood_pressure,
            'diastolic_blood_pressure': self.__diastolic_blood_pressure,
            'temperature': self.__temperature,
            'oxygen_saturation': self.__oxygen_saturation,
            'respiratory_rate': self.__respiratory_rate,
            'glucose': self.__glucose
        }

    def convert_to_json(self):
        return dict(
            id=self.id,
            timestamp=str(self.__timestamp),
            heart_rate=self.__heart_rate,
            systolic_blood_pressure=self.__systolic_blood_pressure,
            diastolic_blood_pressure=self.__diastolic_blood_pressure,
            temperature=self.__temperature,
            oxygen_saturation=self.__oxygen_saturation,
            respiratory_rate=self.__respiratory_rate,
            glucose=self.__glucose,
            anomaly_scores=self.__anomaly_scores
        )