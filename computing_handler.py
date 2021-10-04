import logger
from models.user import User
from models.userResult import UserResult


def computeLevelScores(users: dict[int, User], levelNum) -> list[UserResult]:
    userResults: list[UserResult] = []

    for user in users.values():
        # if not user.hasSubmittedLevel(levelNum):
        #     logger.warningLog(f"User {user} hasnt submitted level: {levelNum}")
        # else:
        #     submittedLevel = user.getSubmittedLevels(levelNum)
        #     submittedLevel.score = calculateUserScore(user.username, submittedLevel.levelIndex)
        userResults.append(UserResult(user.username, 55))

    return userResults

def calculateUserScore(username, levelNum):
    return 55
