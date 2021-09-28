import errno
import os
from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug import datastructures
from level_handler import LevelHandler
from models.user import User
from tools import socketio_server as sio
import logger
from global_data import DataBase

adminPassword = "admin"

app = Flask(__name__)
api = Api(app)

requestHeaderAuthorization = reqparse.RequestParser()
requestHeaderAuthorization.add_argument("Authorization", help="username of the user requesting", required=True,
                                        location='headers')
requestHeaderLevelTime = reqparse.RequestParser()
requestHeaderLevelTime.add_argument("time", help="looking for key: time in the body of the request", required=True,
                                    location='headers')

requestBodyFile = reqparse.RequestParser()
requestBodyFile.add_argument("file", help="looking for file in body", type=datastructures.FileStorage,
                             required=True, location='files')

levelHandler: LevelHandler = LevelHandler(level=DataBase.savedLevels[0])


class Timer(Resource):
    def get(self):
        return levelHandler.timer.timeLeft


class SubmitLevel(Resource):
    def post(self, level):
        args = requestBodyFile.parse_args()
        uploaded_file = args.file
        args = requestHeaderAuthorization.parse_args()
        username = args.Authorization
        file_location = f"submission/level_{level}/user_{DataBase.usersDictionary[username].id}/file.txt"

        if not os.path.exists(os.path.dirname(file_location)):
            try:
                os.makedirs(os.path.dirname(file_location))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        uploaded_file.save(file_location)
        logger.infoLog(f"file '{uploaded_file.filename}' saved at '{file_location}'")


class StopCurrentLevel(Resource):
    def post(self):
        if levelHandler.timer.timeLeft is levelHandler.timer.levelTime:
            logger.infoLog('Cannot stop the level, level hasnt been started')
        else:
            levelHandler.timer.pauseTimer()
            sio.emitEvent(sio.Events.STOP_LEVEL)


class EndCurrentLevel(Resource):
    def post(self):
        if levelHandler.timer.timeLeft is levelHandler.timer.levelTime:
            logger.infoLog('Cannot end the level, level hasnt been started')
        else:
            levelHandler.timer.stopTimer()


class Compute(Resource):
    def post(self):
        return


class StartLevel(Resource):
    def post(self, level):
        if levelHandler.timer.timeLeft is not levelHandler.timer.levelTime:
            logger.infoLog('Cannot Start new level, theres already a level in progress')
        else:
            levelHandler.__init__(DataBase.savedLevels[level - 1])
            levelHandler.timer.countdown()
            sio.emitEvent(sio.Events.START_LEVEL, levelHandler.level)


class GetCurrentLevel(Resource):
    def get(self):
        return {"level": levelHandler.level.levelNumber, "timeLeft": levelHandler.timer.timeLeft}


class Login(Resource):
    def post(self):
        args = requestHeaderAuthorization.parse_args()
        if args.Authorization:
            username = args.Authorization
            logger.debugLog(f'New user just logged in, user: {args.Authorization}')
            userId = len(DataBase.usersDictionary)
            DataBase.usersDictionary[username] = User(id=userId, username=username)
            sio.emitEvent(sio.Events.USER_LOGIN, username)
        else:
            logger.errorLog('Login request header has no username')


class SetLevelTime(Resource):
    def post(self, level):
        args = requestHeaderLevelTime.parse_args()
        DataBase.savedLevels[level - 1].levelTime = args.time


api.add_resource(SubmitLevel, '/submit/<int:level>')
api.add_resource(SetLevelTime, '/setleveltime/<int:level>')
api.add_resource(Timer, '/timer')
api.add_resource(Login, '/login')
api.add_resource(GetCurrentLevel, '/currentLevel')
api.add_resource(StartLevel, '/startLevel/<int:level>')
api.add_resource(StopCurrentLevel, '/stopCurrentLevel')
api.add_resource(EndCurrentLevel, '/endCurrentLevel')
api.add_resource(Compute, '/compute')


def initHttpServer():
    app.run(host='0.0.0.0', port=8080, debug=True)
