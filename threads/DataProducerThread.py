from threading import Thread, Event


class DataProducerThread(Thread):
    def __init__(self, file_reader):
        super().__init__()
        self.__file_reader = file_reader
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.__file_reader.read_data(self.stopped)