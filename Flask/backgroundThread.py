import threading
from queue import Queue
from abc import abstractmethod, ABC

TASKS_QUEUE = Queue()


class BackgroundThread(threading.Thread, ABC):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    @abstractmethod
    def startup(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        raise NotImplementedError()

    def run(self) -> None:
        self.startup()
        while not self._stopped():
            self.handle()
        self.shutdown()
