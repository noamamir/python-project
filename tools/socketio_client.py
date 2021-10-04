from enum import Enum

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


def init():
    sio.connect('http://localhost:15006/', wait=True, wait_timeout=2)
    sio.wait()


def emitEvent(eventName, data=None):
    sio.emit(event=eventName, data=data)


class Events(Enum):
    USER_LOGIN = 'user-login'
    START_LEVEL = 'start-level'
    END_LEVEL = 'end-level'
    CONTINUE_TIMER = 'continue-level'
    STOP_LEVEL = 'stop-level'
    NEXT_LEVEl = 'next-level'
    UPDATE_SCOREBOARD = 'update-scoreboard'
    SET_LEVEL_TIME = 'set-level-time'
