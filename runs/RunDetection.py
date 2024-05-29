from dataReaders.FileReader import FileReader
from window.WindowQueue import WindowQueue
from threads.DataProducerThread import DataProducerThread
from threads.detectionAlgorithms.HalfSpaceTreesDetector import HalfSpaceTreesDetector
from threads.detectionAlgorithms.GaussianScorerDetector import GaussianScorerDetector
from threads.detectionAlgorithms.LocalOutlierFactorDetector import LocalOutlierFactorDetector
from config.config import SLEEP_TIME, WARMUP_PERIOD, THRESHOLD, APPROACH


class RunDetection:
    def __init__(self, file_name, labels_file_name, websocket=None, approach=APPROACH, window_size=WARMUP_PERIOD,
                 threshold=THRESHOLD, sleep_time=SLEEP_TIME):
        self.__queue = WindowQueue(2000)
        self.__approach = approach
        self.__window_size = window_size
        self.__threshold = threshold
        file_reader = FileReader(file_name, labels_file_name, self.__queue, sleep_time=sleep_time)
        self.__producer_thread = DataProducerThread(file_reader)
        self.__consumer_thread = None

        self.init_consumer(websocket)

    def init_consumer(self, websocket):
        if self.__approach == 'half_space_trees':
            self.__consumer_thread = HalfSpaceTreesDetector(self.__queue, websocket=websocket,
                                                            threshold=self.__threshold, window_size=self.__window_size)
        elif self.__approach == 'gaussian_scorer':
            self.__consumer_thread = GaussianScorerDetector(self.__queue, websocket=websocket,
                                                            threshold=self.__threshold, window_size=self.__window_size)
        elif self.__approach == 'local_outlier_factor':
            detector = LocalOutlierFactorDetector(self.__queue, websocket=websocket, threshold=self.__threshold,
                                                  window_size=self.__window_size)
            self.__consumer_thread = detector
        else:
            raise ValueError('Invalid approach')

    def stop(self):
        self.__producer_thread.stop()
        self.__consumer_thread.stop()

    def run(self):
        self.__producer_thread.start()
        self.__consumer_thread.start()

        self.__producer_thread.join()
        self.__consumer_thread.join()
