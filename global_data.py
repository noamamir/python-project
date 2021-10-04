# saves global variables acting as database
from level_handler import LevelHandler
from models import scoreboard
from models.level import Level
from models.scoreboard import Scoreboard
from models.user import User


class DataBase:
    def __init__(self):
        self.scoreboards: dict[Scoreboard] = {}
        self.usersDictionary: dict[int, User] = {0: User('noam1', 1), 1: User('noam2', 1)}
        self.savedLevels = [Level(levelNumber=1, levelMaxPoints=100, levelTime=60),
                            Level(levelNumber=2, levelMaxPoints=100, levelTime=1800),
                            Level(levelNumber=3, levelMaxPoints=100, levelTime=1800),
                            Level(levelNumber=4, levelMaxPoints=100, levelTime=1800)]

    def hasUser(self, username):
        if username in self.usersDictionary:
            return True
        return False

    def getUser(self, username) -> User:
        return self.usersDictionary[username]

    def hasScoreboard(self, levelNum):
        return levelNum in self.scoreboards
