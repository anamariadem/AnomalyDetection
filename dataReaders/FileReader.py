import csv
import time

from models.PatientVitalsTuple import PatientVitalsTuple


class FileReader:
    def __init__(self, file_name, queue):
        self.__file_name = file_name
        self.__queue = queue

    def read_data(self, stopped):
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
                vitals_tuple = PatientVitalsTuple(row[0], row[1], float(row[2]), float(row[3]),
                                                  float(row[4]), float(row[5]), float(row[6]), float(row[7]),
                                                  float(row[8]))

                self.__queue.push(vitals_tuple)

                line += 1
                time.sleep(0.1)
