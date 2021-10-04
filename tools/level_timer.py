import threading
import time
from datetime import datetime
import tkinter  as tk
from tools import socketio_server as sio

check = threading.Condition()


class LevelTimer:
    def __init__(self, levelTime):
        self.__pauseSignal = False
        self.levelTime = levelTime
        self.timeLeft = levelTime
        now = datetime.now()
        self.initTime = now.strftime("%H:%M:%S")
        self.timeoutSignal = False

    def timerPaused(self):
        return self.__pauseSignal

    def stopTimer(self):
        self.__pauseSignal = False
        self.timeLeft = 0

    def pauseTimer(self):
        self.__pauseSignal = True

    def getTimeLeft(self):
        return self.timeLeft

    def continueTimer(self):
        self.__pauseSignal = False
        self.timeoutSignal = False

    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def timeout(self):
        self.timeoutSignal = True
        sio.emitEvent(sio.Events.END_LEVEL)


    def countdown(self, remaining=None):
        while True:
            if self.__pauseSignal is not False:
                pass
            elif self.timeLeft > 0:
                mins, secs = divmod(self.timeLeft, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                time.sleep(1)
                self.timeLeft -= 1
            elif self.timeoutSignal is False:
                self.pauseTimer()
                self.timeout()


timer: LevelTimer = LevelTimer(1800)


def initDefualtTimer():
    timer.__init__(1800)


def initTimer(seconds):
    timer.__init__(seconds)


def getTimer():
    return timer
