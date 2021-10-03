from enum import Enum
import socketio
import eventlet
from eventlet import wsgi
import logger


# Init server
serverio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(serverio)


def emitEvent(eventName, data=None):
    serverio.emit(data=data, event=eventName)


def initSocketioServer():
    logger.infoLog(f'starting socketIo server on port 15006')
    eventlet.wsgi.server(eventlet.listen(('', 15006)), app)



class Events(Enum):
    USER_LOGIN = 'user-login'
    START_LEVEL = "start-level"
    END_LEVEL = 'end-level'
    CONTINUE_TIMER = 'continue-level'
    STOP_LEVEL = 'stop-level'
    NEXT_LEVEl = 'next-level'
    UPDATE_SCOREBOARD = 'update-scoreboard'
    NEW_USER_SUBMISSION = 'new-user-submission'


@serverio.event()
def connect(sid, enviorment):
    print(sid, ': a client has connection')


@serverio.event()
def disconnect(sid):
    print(sid, ': a client has disconnected')


@serverio.on('*')
def check_event(sid, data):
    print(f"emitted event, data: {data}")

@serverio.on(Events.START_LEVEL.value)
def START_LEVEL(sid, data):
    logger.infoLog("Emitted start level event!!!!!!!!!!!!!!!!")
    return data

#
#
# @serverio.on(Events.CONTINUE_TIMER.value)
# async def CONTINUE_TIMER(sid, data):
#     return data
#
#
# @serverio.on(Events.NEXT_LEVEl.value)
# async def NEXT_LEVEl(sid, data):
#     return data
#
#
# @serverio.on(Events.STOP_LEVEL.value)
# async def STOP_LEVEL(sid, data):
#     return data
#
#
# @serverio.on(Events.UPDATE_SCOREBOARD.value)
# async def STOP_LEVEL(sid, data):
#     return data
#
#
# @serverio.on(Events.USER_LOGIN.value)
# async def USER_LOGIN(sid, data):
#     return data
#
#
# @serverio.on(Events.NEW_USER_SUBMISSION.value)
# async def NEW_USER_SUBMISSION(sid, data):
#     return data
