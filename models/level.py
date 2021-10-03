import json


class Level:
    def __init__(self, levelNumber, levelMaxPoints, levelTime=1800):
        self.levelNumber = levelNumber
        self.levelTime = levelTime
        self.levelMaxPoints = levelMaxPoints

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)