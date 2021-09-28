# This is a sample Python script.
import rest_api
from threading import Thread

import global_data
import logging

from tools import socketio_server

if __name__ == '__main__':
    Thread(target=rest_api.initHttpServer()).start()
    Thread(target=socketio_server.initSocketioServer(15006)).start()

