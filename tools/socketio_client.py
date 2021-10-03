import socketio

sio = socketio.AsyncClient()


async def emitEvent(eventName, data=None):
    await sio.emit(event=eventName, data=data)


@sio.on('*')
async def catch_all(event, sid, data):
    pass


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


async def initClient():
    await sio.connect('http://localhost:15006')
    await sio.wait()
    print('my sid is', sio.sid)