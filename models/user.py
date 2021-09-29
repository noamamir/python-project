from models.submittedLevel import SubmittedLevel


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.submittedLevels: dict[SubmittedLevel] = {}

    def hasSubmittedLevel(self, levelIndex) -> bool:
        if levelIndex in self.submittedLevels:
            return True
        return False

    def getSubmittedLevels(self, levelIndex) -> SubmittedLevel:
        return self.submittedLevels[levelIndex]

    def submitLevel(self, level: SubmittedLevel):
        self.submittedLevels[level.levelIndex] = level
