# This is a sample Python script.
from threading import Thread
from queue import Queue
import rest_api
from tools import socketio_server
from tools import level_timer as timer

if __name__ == '__main__':
    q = Queue()
    Thread(target=rest_api.initHttpServer).start()
    Thread(target=socketio_server.initSocketioServer).start()
    Thread(target=timer.initTimer).start()
