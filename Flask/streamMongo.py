import pymongo
from Flask.methodsMongoDb import MethodsCollection
from Flask.backgroundThread import BackgroundThread
import logging
from queue import Queue
import time
import queue

TASKS_QUEUE = Queue()


class streams(BackgroundThread):

    def __init__(self, method_graph, name):
        super().__init__()

        self.method_graph = method_graph
        self.name = name

        method = MethodsCollection()
        self.collection = method.get_collection(name)

    def insert_change_stream(self):

        accounts_collection = self.collection

        try:
            resume_token = None
            pipeline = [{'$match': {'operationType': 'insert'}}]
            with accounts_collection.watch(pipeline) as stream:
                for update_change in stream:
                    #
                    #
                    # UPDATE DYNAMIC GRAPH
                    #
                    self.method_graph.update_graph(update_change["fullDocument"])
                    #
                    resume_token = stream.resume_token

        except pymongo.errors.PyMongoError:
            if resume_token is None:
                logging.error('...')
            else:
                with accounts_collection.watch(pipeline, resume_after=resume_token) as stream:
                    for update_change in stream:
                        print(update_change)

    def startup(self) -> None:
        print(self.name)
        logging.info('NotificationThread started')
        self.insert_change_stream()

    def shutdown(self) -> None:
        logging.info('NotificationThread stopped')

    def handle(self) -> None:
        try:
            task = TASKS_QUEUE.get(block=False)
            logging.info(f'Notification for {task} was sent.')
        except queue.Empty:
            time.sleep(1)
