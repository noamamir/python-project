import json

from models.userResult import UserResult


class Scoreboard:
    def __init__(self, levelMaxPoints, scores: list[UserResult] = None):
        self.scores = scores
        self.levelMaxPoints = levelMaxPoints

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
