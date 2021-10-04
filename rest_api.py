import errno
import os
import threading
import json
import time
from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from werkzeug import datastructures

import computing_handler
import logger
from global_data import DataBase
from level_handler import LevelHandler
from models.level import Level
from models.scoreboard import Scoreboard
from models.submittedLevel import SubmittedLevel
from models.user import User
from tools import level_timer as timer
from tools import socketio_client as sio

adminPassword = 'IAMTHEMANAGER'

database = DataBase()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"*": {"origins": "*"}})

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

levelHandler: LevelHandler = LevelHandler(level=database.savedLevels[0])
check = threading.Condition()


class Timer(Resource):
    def get(self):
        print(timer.getTimer().timeLeft)
        return timer.getTimer().timeLeft


class SubmitLevel(Resource):
    def post(self, levelNum):
        uploaded_file = requestBodyFile.parse_args().file
        username = requestHeaderAuthorization.parse_args().Authorization

        if database.hasUser(username):
            file_location = f"submission/level_{levelNum}/user_{database.usersDictionary[username].id}/file.py"
            submittedLevel = SubmittedLevel(timer.getTimer().getCurrentTime(), timeLeft=timer.getTimer().timeLeft,
                                            levelPath=file_location, levelIndex=levelNum)
            database.getUser(username).submitLevel(submittedLevel)

            if not os.path.exists(os.path.dirname(file_location)):
                try:
                    os.makedirs(os.path.dirname(file_location))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            uploaded_file.save(file_location)
            logger.infoLog(f"file '{uploaded_file.filename}' saved at '{file_location}'")
        else:
            logger.errorLog("Couldnt find user, please login again")


class StopCurrentLevel(Resource):
    def post(self):
        password = requestHeaderAuthorization.parse_args().Authorization
        if password == adminPassword:
            if timer.getTimer().timeLeft is timer.getTimer().levelTime:
                logger.warningLog('Cannot stop the level, level hasnt been started')
            else:
                timer.getTimer().pauseTimer()
                sio.emitEvent(sio.Events.STOP_LEVEL.value)
                logger.infoLog(f'level paused, timer stopped at {timer.getTimer().timeLeft}')
        else:
            logger.warningLog('Password sent doesnt match the admin password')


class EndCurrentLevel(Resource):
    def post(self):
        password = requestHeaderAuthorization.parse_args().Authorization
        if password == adminPassword:
            if timer.getTimer().timeLeft is timer.getTimer().levelTime:
                logger.infoLog('Cannot end the level, level hasnt been started')
            else:
                logger.infoLog('level ended, timer stopped')
                timer.getTimer().stopTimer()
                sio.emitEvent(sio.Events.END_LEVEL.value)
        else:
            logger.warningLog('Password sent doesnt match the admin password')


class Compute(Resource):
    def post(self):
        password = requestHeaderAuthorization.parse_args().password
        if password == adminPassword:
            compute()
        else:
            logger.warningLog('Password sent doesnt match the admin password')
        return


class StartLevel(Resource):
    def post(self, level):
        password = requestHeaderAuthorization.parse_args().Authorization
        if password == adminPassword:
            if levelHandler.level.levelNumber == level and timer.getTimer().timerPaused():
                logger.infoLog(f'Continuing level {level}, timer continues at: {timer.getTimer().timeLeft}')
                timer.getTimer().continueTimer()
                currentLevelState = Level(levelNumber=levelHandler.level.levelNumber,
                                          levelTime=timer.getTimer().timeLeft)
                sio.emitEvent(sio.Events.START_LEVEL.value, currentLevelState.toJSON())
            else:
                if timer.getTimer().timeLeft is not timer.getTimer().levelTime:
                    logger.infoLog('Cannot Start a new level, theres already a level in progress')
                else:
                    initNewLevel(level)
        else:
            logger.warningLog('Password sent doesnt match the admin password')


def initNewLevel(levelNum):
    levelToStart = database.savedLevels[levelNum - 1]
    levelHandler.__init__(levelToStart)
    timer.initTimer(levelToStart.levelTime)
    logger.infoLog(f'Starting a new level, timer started for level {levelNum}')
    sio.emitEvent(sio.Events.START_LEVEL.value, levelHandler.level.toJSON())
    threading.Thread(target=timer.getTimer().countdown).start()


class GetCurrentLevel(Resource):
    def get(self):
        return {"level": levelHandler.level.levelNumber, "timeLeft": timer.getTimer().timeLeft}


class GetIsLevelRunning(Resource):
    def get(self, level):
        password = requestHeaderAuthorization.parse_args().Authorization
        if password == adminPassword:
            if levelHandler.level.levelNumber == level and not timer.getTimer().timerPaused() and timer.getTimer().timeLeft is not timer.getTimer().levelTime:
                return True
            else:
                return False
        else:
            logger.warningLog('Password sent doesnt match the admin password')
            return None


class Login(Resource):
    def post(self):
        args = requestHeaderAuthorization.parse_args()
        if args.Authorization:
            username = args.Authorization
            logger.debugLog(f'New user just logged in, user: {args.Authorization}')
            userId = len(database.usersDictionary)
            database.usersDictionary[username] = User(id=userId, username=username)
            sio.emitEvent(sio.Events.USER_LOGIN.value, username)
        else:
            logger.errorLog('Login request header has no username')


class SetLevelTime(Resource):
    def post(self, level):
        password = requestHeaderAuthorization.parse_args().Authorization
        if password == adminPassword:
            time = request.data
            database.savedLevels[level - 1].levelTime = int(time) * 60
        else:
            logger.warningLog('Password sent doesnt match the admin password')


class GetSubmissionTime(Resource):
    def get(self, level):
        args = requestHeaderAuthorization.parse_args()
        username = args.Authorization

        if database.hasUser(username) and database.getUser(username).hasSubmittedLevel(level):
            print(database.getUser(username).getSubmittedLevels(level).completionTime)
            return database.getUser(username).getSubmittedLevels(level).completionTime

        logger.warningLog('Couldnt get submittion time, user or level submittion invalid')

        return None


class GetScoreboard(Resource):
    def get(self, level):
        if database.hasScoreboard(level):
            logger.infoLog(f'Returning scoreboard for level: {level}')
            return database.scoreboards.get(level)
        else:
            logger.warningLog(f'Couldnt get scoreboard for level :{level}, scoreboard doesnt exist')
            return None


def computeAtTimeout():
    while True:
        if timer.getTimer().timeoutSignal:
            compute()
            initNewLevel(levelHandler.level.levelNumber + 1)
            timer.getTimer().timeoutSignal = False
        time.sleep(1)


def compute():
    levelNumber = levelHandler.level.levelNumber
    logger.infoLog(f"Computing user results for level {levelNumber}")
    levelUserResults = computing_handler.computeLevelScores(database.usersDictionary, levelNumber)
    levelScoreboard: Scoreboard = Scoreboard(levelMaxPoints=database.savedLevels[levelNumber - 1].levelMaxPoints,
                                             scores=levelUserResults)
    database.scoreboards[levelNumber] = levelScoreboard
    logger.infoLog(f"Successfully generated scoreboard for level {levelNumber}")
    sio.emitEvent(sio.Events.UPDATE_SCOREBOARD.value, levelScoreboard.toJSON())


class GetResult(Resource):
    def get(self, levelNum):
        args = requestHeaderAuthorization.parse_args()
        username = args.Authorization
        files: dict = {}
        levelIndex = levelNum - 1

        for filename in os.listdir(f"Results/{levelIndex}/{database.usersDictionary[username].id}"):
            with open(os.path.join(f"Results/{levelIndex}/{database.usersDictionary[username].id}", filename), 'r') as f:
                files[filename] = f.read()

        return files


api.add_resource(GetResult, '/result/<int:levelNum>')
api.add_resource(GetScoreboard, '/scoreboard/<int:level>')
api.add_resource(GetSubmissionTime, '/submissionTime/<int:level>')
api.add_resource(SubmitLevel, '/submit/<int:levelNum>')
api.add_resource(SetLevelTime, '/setLevelTime/<int:level>')
api.add_resource(Timer, '/timeLeft')
api.add_resource(Login, '/login')
api.add_resource(GetCurrentLevel, '/currentLevel')
api.add_resource(GetIsLevelRunning, '/isRunning/<int:level>')
api.add_resource(StartLevel, '/startLevel/<int:level>')
api.add_resource(StopCurrentLevel, '/stopCurrentLevel')
api.add_resource(EndCurrentLevel, '/endCurrentLevel')
api.add_resource(Compute, '/compute')


def initHttpServer(in_q):
    threading.Thread(target=computeAtTimeout).start()
    app.run(host='0.0.0.0', port=8081, debug=True, use_reloader=False)
