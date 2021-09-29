# saves global variables acting as database
from level_handler import LevelHandler
from models import scoreboard
from models.level import Level
from models.user import User


class DataBase:
    def __init__(self):
        self.usersDictionary: dict[User] = {}
        self.savedLevels = [Level(levelNumber=1, levelMaxPoints=100), Level(levelNumber=2, levelMaxPoints=60),
                            Level(levelNumber=3, levelMaxPoints=60), Level(levelNumber=4, levelMaxPoints=60)]

    def hasUser(self, username):
        if username in self.usersDictionary:
            return True
        return False

    def getUser(self, username) -> User:
        return self.usersDictionary[username]
