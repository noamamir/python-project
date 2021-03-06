# saves global variables acting as database
from level_handler import LevelHandler
from models import scoreboard
from models.level import Level
from models.scoreboard import Scoreboard
from models.user import User


class DataBase:
    def __init__(self):
        self.scoreboards: dict[Scoreboard] = {}
        self.usersDictionary: dict[int, User] = {0: User(1, 'noam1'), 1: User(2, 'noam2')}
        self.savedLevels = [Level(levelNumber=1, levelMaxPoints=100, levelTime=20),
                            Level(levelNumber=2, levelMaxPoints=100, levelTime=1800),
                            Level(levelNumber=3, levelMaxPoints=100, levelTime=1800)]

    def hasUser(self, username):
        return username in self.usersDictionary

    def getUser(self, username) -> User:
        return self.usersDictionary[username]

    def hasScoreboard(self, levelNum):
        return levelNum in self.scoreboards
