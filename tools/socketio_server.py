from enum import Enum
import socketio
import eventlet
from eventlet import wsgi
import logger

# Init server
serverio = socketio.Server()
app = socketio.WSGIApp(serverio)

def emitEvent(eventName, data=None):
    serverio.emit(data=data, event=eventName)


def initSocketioServer():
    logger.infoLog(f'starting socketIo servoer on port 15006')
    eventlet.wsgi.server(eventlet.listen(('', 15006)), app)


@serverio.event()
def connect(sid, enviorment):
    print(sid, ': a client has connection')


@serverio.event()
def disconnect(sid):
    print(sid, ': a client has disconnected')


@serverio.on('start-level')
async def start_level(sid, data):
    return data


class Events(Enum):
    USER_LOGIN = 'user-login'
    START_LEVEL = 'start-level'
    END_LEVEL = 'end-level'
    CONTINUE_TIMER = 'continue-level'
    STOP_LEVEL = 'stop-level'
    NEXT_LEVEl = 'next-level'
    UPDATE_SCOREBOARD = 'update-scoreboard'
