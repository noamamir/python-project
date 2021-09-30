from tools.level_timer import LevelTimer
from models.scoreboard import Scoreboard
from models.level import Level


class LevelHandler:
    def __init__(self, level: Level):
        self.level = level
        self.scoreboard: Scoreboard = Scoreboard(levelMaxPoints=level.levelMaxPoints)

