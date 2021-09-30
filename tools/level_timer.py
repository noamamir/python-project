import time
from datetime import datetime
import tkinter as tk
from tools import socketio_server as sio


def timeout():
    sio.emitEvent(sio.Events.END_LEVEL)

root = tk.Tk()

class LevelTimer():
    def __init__(self, levelTime):
        self.__pauseSignal = False
        self.levelTime = levelTime
        self.timeLeft = levelTime



        now = datetime.now()
        self.initTime = now.strftime("%H:%M:%S")

    def stopTimer(self):
        self.timeLeft = 0

    def pauseTimer(self):
       pass

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
        if remaining is not None:
            self.timeLeft = remaining
        if self.timeLeft <= 0:
            timeout()
        else:
            self.timeLeft = self.timeLeft - 1
            root.after(1000, self.countdown)
