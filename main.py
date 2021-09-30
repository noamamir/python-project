# This is a sample Python script.
from threading import Thread

import rest_api
from tools import socketio_server

if __name__ == '__main__':
    rest_api.initHttpServer()
    Thread(target=socketio_server.initSocketioServer(15006)).start()
