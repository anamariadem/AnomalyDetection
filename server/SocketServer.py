import websockets
import asyncio
import json
import threading

from runs.RunDetection import RunDetection


class SocketServer:
    def __init__(self):
        self.server_socket = None
        self.__detector_processor = None
        self.__thread = None

    async def start(self):
        async with websockets.serve(self.socket_handler, 'localhost', 8001):
            print(f"Websocket server started at localhost 8001")
            await asyncio.Future()  # Run forever

    def handle_start_execution(self, websocket, approach):
        self.__detector_processor = RunDetection('./inputData/new_dataset_with_labels.csv', './inputData/labels/anomaly_labels.csv',
                                                 approach=approach, websocket=websocket)
        self.__detector_processor.run()

    def handle_stop_execution(self):
        self.__detector_processor.stop()

    async def socket_handler(self, websocket, path):
        print('-->', websocket, path)
        while True:
            try:
                message = await websocket.recv()

                print('message', message)

                if message == 'connected':
                    continue

                event_object = json.loads(message)
                event = event_object["event"]

                if event == 'start':
                    self.__thread = threading.Thread(target=self.handle_start_execution, args=(websocket, event_object['approach']))
                    self.__thread.start()
                elif event == 'stop':
                    self.handle_stop_execution()
                    self.__thread.join()

            except websockets.ConnectionClosed as e:
                print('Client disconnected', e)
                break


socket_server = SocketServer()
asyncio.run(socket_server.start())
