from Flask.streamMongo import streams
from queue import Queue

TASKS_QUEUE = Queue()


class BackgroundThreadFactory:
    @staticmethod
    def create(graph) -> list[streams]:
        array = []
        names = ['government', 'health', 'economy', 'environment', 'education', 'business',
                 'sport', 'entertainment', ]

        for name in names:
            array.append(streams(graph, name))

        return array
