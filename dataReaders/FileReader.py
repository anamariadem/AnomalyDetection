import csv
import time

from models.PatientVitalsTuple import PatientVitalsTuple
from config.config import SLEEP_TIME


class FileReader:
    def __init__(self, file_name, labels_file_name, queue, sleep_time=SLEEP_TIME):
        self.__file_name = file_name
        print('file name:', file_name)
        self.__queue = queue
        self.__sleep_time = sleep_time
        self.__labels_file_name = labels_file_name
        print('labels file name:', labels_file_name)

    def read_data(self, stopped):
        label_data = []
        with open(self.__labels_file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                label_data.append(row)

        with open(self.__file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line = 0

            for row in csv_reader:
                if stopped():
                    return
                if line == 0:
                    line += 1
                    continue

                if len(row) != 9:
                    continue

                print('read:', row[0])
                labels_tuple = label_data[line]
                anomaly_labels = {
                    'heart_rate': int(float(labels_tuple[1])),
                    'systolic_blood_pressure': int(float(labels_tuple[2])),
                    'diastolic_blood_pressure': int(float(labels_tuple[3])),
                    'temperature': int(float(labels_tuple[4])),
                    'oxygen_saturation': int(float(labels_tuple[5])),
                    'respiratory_rate': int(float(labels_tuple[6])),
                    'glucose': int(float(labels_tuple[7]))
                }

                vitals_tuple = PatientVitalsTuple(row[0], row[1], float(row[2]), float(row[3]),
                                                  float(row[4]), float(row[5]), float(row[6]), float(row[7]),
                                                  float(row[8]), anomaly_labels)

                self.__queue.push(vitals_tuple)

                line += 1
                time.sleep(self.__sleep_time)

        while not stopped():
            time.sleep(self.__sleep_time)
