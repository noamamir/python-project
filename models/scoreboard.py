from models.userResult import UserResult


class Scoreboard:
    def __init__(self, levelMaxPoints, scores:list[UserResult] = None):
        self.scores = scores
        self.levelMaxPoints = levelMaxPoints

