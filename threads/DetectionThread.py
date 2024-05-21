from threading import Thread, Event
import asyncio
import json

from utils.plot import plot_detection_results
from utils.save_to_csv import save_anomaly_score_to_csv
from utils.metrics import set_metrics
from config.warmup import WARMUP_PERIOD


class DetectionThread(Thread):
    def __init__(self, queue, websocket=None):
        super().__init__()
        self.__queue = queue
        self.__websocket = websocket

        self.__processed_tuples = []
        self._detector = None
        self._detectors = {}
        self._stop_event = Event()

    def learn_one(self, processing_tuple_dict):
        pass

    def score_one(self, processing_tuple_dict):
        pass

    async def process_tuple(self, processing_tuple):
        processing_tuple_dict = processing_tuple.to_dict()
        print('Processing tuple:', processing_tuple.id)

        if int(processing_tuple.id) > WARMUP_PERIOD:
            results = self.score_one(processing_tuple_dict)
            processing_tuple.set_anomaly_score_dict(results)
            set_metrics(processing_tuple)

            print("{:<8} {:<15}".format('Key', 'Score'))
            for key, result in processing_tuple.anomaly_scores.items():
                print("{:<8} {:<15}".format(key, result))
            print('\n')

            if self.__websocket is not None:
                data_to_send = json.dumps(dict(type='processed_tuples', data=processing_tuple.convert_to_json()))
                await self.__websocket.send(data_to_send)
        else:
            if self.__websocket is not None:
                data_to_send = json.dumps(
                    dict(type='warmup_update', data={'warmup': int(processing_tuple.id) / WARMUP_PERIOD}))
                await self.__websocket.send(data_to_send)

        self.learn_one(processing_tuple_dict)
        self.__processed_tuples.append(processing_tuple)

    def handle_thread_stop(self):
        plot_detection_results(self.__processed_tuples)
        save_anomaly_score_to_csv(self.__processed_tuples)

    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    async def process_data(self):
        while True:
            if self.stopped():
                self.handle_thread_stop()
                break

            if len(self.__queue) > 0:
                # self.__queue.print()
                await self.process_tuple(self.__queue.pop())

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.process_data())
        loop.close()
