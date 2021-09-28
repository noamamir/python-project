import time
from tkinter import Tk
from tools import socketio_server as sio


def timeout():
    sio.emitEvent(sio.Events.END_LEVEL)


class LevelTimer:
    def __init__(self, levelTime):
        self.__root = Tk()
        self.__pauseSignal = False
        self.levelTime = levelTime
        self.timeLeft = levelTime
        self.initTime = time.time()

    def stopTimer(self):
        self.timeLeft = 0

    def pauseTimer(self):
        self.__pauseSignal = True

    def getTimeLeft(self):
        return self.timeLeft

    def continueTimer(self):
        self.__pauseSignal = False
        self.countdown()

    def countdown(self, remaining=None):
        if remaining is not None:
            self.timeLeft = remaining

        if self.timeLeft <= 0:
            timeout()
        elif not self.__pauseSignal:
            self.timeLeft = self.timeLeft - 1
            self.__root.after(1000, self.countdown)
