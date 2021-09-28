# saves global variables acting as database
from level_handler import LevelHandler
from models import scoreboard
from models.level import Level
from models.user import User


class DataBase:
    usersDictionary = {}
    savedLevels = [Level(levelNumber=1, levelMaxPoints=60), Level(levelNumber=2, levelMaxPoints=60),
                   Level(levelNumber=3, levelMaxPoints=60), Level(levelNumber=4, levelMaxPoints=60)]
