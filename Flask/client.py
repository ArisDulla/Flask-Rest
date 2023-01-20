from pymongo import MongoClient

from MongoDb.info import InfoData


class ClientMongo:

    def __init__(self):
        self.mongoClient = MongoClient(InfoData.mongoInfo,
                                       maxPoolSize=7200,  # connection pool size is 200
                                       waitQueueTimeoutMS=13200,  # how long a thread can wait for a connection
                                       waitQueueMultiple=13500)  # when the pool is fully used 200 threads can wait
