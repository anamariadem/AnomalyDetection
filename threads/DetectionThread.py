from threading import Thread, Event
import asyncio
import json
from river import metrics

from utils.plot import plot_detection_results
from utils.save_to_csv import save_metrics_to_csv
from utils.metrics import set_metrics
from utils.print import print_anomaly_scores
from config.config import WARMUP_PERIOD, THRESHOLD


class DetectionThread(Thread):
    def __init__(self, queue, websocket=None):
        super().__init__()
        self.__queue = queue
        self.__websocket = websocket
        self._threshold = THRESHOLD
        self._window_size = WARMUP_PERIOD
        self._approach = None

        self.__processed_tuples = []
        self._detector = None
        self._detectors = {}
        self._auc_scores = {
            'heart_rate': metrics.ROCAUC(),
            'systolic_blood_pressure': metrics.ROCAUC(),
            'diastolic_blood_pressure': metrics.ROCAUC(),
            'temperature': metrics.ROCAUC(),
            'respiratory_rate': metrics.ROCAUC(),
            'oxygen_saturation': metrics.ROCAUC(),
            'glucose': metrics.ROCAUC(),
        }
        self._precision_scores = {
            'heart_rate': metrics.Precision(),
            'systolic_blood_pressure': metrics.Precision(),
            'diastolic_blood_pressure': metrics.Precision(),
            'temperature': metrics.Precision(),
            'respiratory_rate': metrics.Precision(),
            'oxygen_saturation': metrics.Precision(),
            'glucose': metrics.Precision(),
        }
        self._recall_scores = {
            'heart_rate': metrics.Recall(),
            'systolic_blood_pressure': metrics.Recall(),
            'diastolic_blood_pressure': metrics.Recall(),
            'temperature': metrics.Recall(),
            'respiratory_rate': metrics.Recall(),
            'oxygen_saturation': metrics.Recall(),
            'glucose': metrics.Recall(),
        }
        self._stop_event = Event()

    def learn_one(self, processing_tuple_dict):
        pass

    def score_one(self, processing_tuple_dict) -> dict:
        pass

    def compute_auc(self, processing_tuple, results):
        for key, result in results.items():
            if key in self._auc_scores:
                self._auc_scores[key].update(y_true=processing_tuple.anomaly_labels[key], y_pred=result)

        auc_scores_to_set = {}
        for key in self._auc_scores.keys():
            auc_scores_to_set[key] = self._auc_scores[key].get()

        processing_tuple.set_auc_score_dict(auc_scores_to_set)

    def compute_precision_and_recall(self, processing_tuple, results):
        for key, result in results.items():
            if key in self._precision_scores:
                predicted_label = 1 if result > self._threshold else 0
                self._precision_scores[key].update(y_true=processing_tuple.anomaly_labels[key], y_pred=predicted_label)
                self._recall_scores[key].update(y_true=processing_tuple.anomaly_labels[key], y_pred=predicted_label)

        precision_scores_to_set = {}
        for key in self._precision_scores.keys():
            precision_scores_to_set[key] = self._precision_scores[key].get()

        recall_scores_to_set = {}
        for key in self._recall_scores.keys():
            recall_scores_to_set[key] = self._recall_scores[key].get()

        processing_tuple.set_precision_score_dict(precision_scores_to_set)
        processing_tuple.set_recall_score_dict(recall_scores_to_set)

    async def process_tuple(self, processing_tuple):
        processing_tuple_dict = processing_tuple.to_dict()
        print('Processing tuple:', processing_tuple.id)

        if int(processing_tuple.id) > self._window_size:
            results = self.score_one(processing_tuple_dict)
            processing_tuple.set_anomaly_score_dict(results)
            set_metrics(processing_tuple)

            self.compute_auc(processing_tuple, results)
            self.compute_precision_and_recall(processing_tuple, results)

            print_anomaly_scores(processing_tuple)

            if self.__websocket is not None:
                data_to_send = json.dumps(dict(type='processed_tuples', data=processing_tuple.convert_to_json()))
                await self.__websocket.send(data_to_send)
        else:
            if self.__websocket is not None:
                data_to_send = json.dumps(
                    dict(type='warmup_update', data={'warmup': int(processing_tuple.id) / self._window_size}))
                await self.__websocket.send(data_to_send)

        self.learn_one(processing_tuple_dict)
        self.__processed_tuples.append(processing_tuple)

    async def handle_thread_stop(self):
        print('STOPPING THREAD')
        if len(self.__queue) > 0:
            print('PROCESSING REMAINING DATA:', len(self.__queue))
            queue = self.__queue.to_list()
            for processing_tuple in queue:
                await self.process_tuple(processing_tuple)
            print('FINISHED PROCESSING REMAINING DATA:', len(self.__queue))

        print('Plotting results and saving data...')
        plot_detection_results(self.__processed_tuples)
        save_metrics_to_csv(self.__processed_tuples, self._approach, self._window_size, self._threshold)

    def stopped(self):
        return self._stop_event.is_set()

    def stop(self):
        self._stop_event.set()

    async def process_data(self):
        while True:
            if self.stopped():
                await self.handle_thread_stop()
                break

            if len(self.__queue) > 0:
                # self.__queue.print()
                await self.process_tuple(self.__queue.pop())

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.process_data())
        loop.close()
