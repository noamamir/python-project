# This is a sample Python script.
import asyncio
import json
import threading
from threading import Thread
from queue import Queue
import requests

import sio as sio
import socketio

import rest_api
from tools import socketio_server, socketio_client
from tools import level_timer as timer

async def initEverything():
    Thread(target=rest_api.initHttpServer).start()
    Thread(target=timer.initDefualtTimer).start()
    thread = threading.Thread(target=between_callback)
    thread.start()

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(socketio_client.initClient())
    loop.close()

if __name__ == '__main__':
    asyncio.run(initEverything())

