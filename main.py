from threading import Thread
import rest_api
from tools import socketio_client
from tools import level_timer as timer


def initEverything():
    Thread(target=rest_api.initHttpServer).start()
    Thread(target=timer.initDefualtTimer).start()
    Thread(target=socketio_client.init).start()



if __name__ == '__main__':
    initEverything()
