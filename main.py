# This is a sample Python script.
from queue import Queue
from threading import Thread
import rest_api
from tools import socketio_client
from tools import level_timer as timer


def initEverything():
    q = Queue()
    Thread(target=rest_api.initHttpServer, args =(q, )).start()
    Thread(target=timer.initDefualtTimer).start()
    Thread(target=socketio_client.init).start()



if __name__ == '__main__':
    initEverything()
