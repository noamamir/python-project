# This is a sample Python script.
import asyncio
import json
import threading
from threading import Thread

import socketio
from socketIO_client_nexus import SocketIO
import sio as sio
import rest_api
from tools import socketio_server, socketio_client
from tools import level_timer as timer


def initEverything():
    Thread(target=rest_api.initHttpServer).start()
    Thread(target=timer.initDefualtTimer).start()
    Thread(target=socketio_client.init).start()



if __name__ == '__main__':
    initEverything()
