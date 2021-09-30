import time
from datetime import datetime
import tkinter  as tk
from tools import socketio_server as sio

class LevelTimer:
    def __init__(self, levelTime):
        self.__pauseSignal = False
        self.levelTime = levelTime
        self.timeLeft = levelTime
        now = datetime.now()
        self.initTime = now.strftime("%H:%M:%S")

    def timerPaused(self):
        return self.__pauseSignal

    def stopTimer(self):
        self.timeLeft = 0

    def pauseTimer(self):
        self.__pauseSignal = True

    def getTimeLeft(self):
        return self.timeLeft

    def continueTimer(self):
        self.__pauseSignal = False
        self.countdown()

    def getCurrentTime(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def countdown(self, remaining=None):
        while self.timeLeft:
            if self.__pauseSignal is not False:
                break
            elif self.timeLeft > 0:
                mins, secs = divmod(self.timeLeft, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                time.sleep(1)
                self.timeLeft -= 1
            else:
                timeout()


timer: LevelTimer = LevelTimer(1800)


def timeout():
    sio.emitEvent(sio.Events.END_LEVEL)


def initTimer():
    timer.__init__(1800)


def getTimer():
    return timer
