import logger
from models.user import User
from models.userResult import UserResult


def computeLevelScores(users: dict[str, User], levelNum) -> list[UserResult]:
    userResults: list[UserResult] = []

    for user in users.values():
        userScore = 0
        if not user.hasSubmittedLevel(levelNum):
            logger.warningLog(f"User {user} hasnt submitted level: {levelNum}")
        else:
            submittedLevel = user.getSubmittedLevels(levelNum)
            userScore = submittedLevel.score = calculateUserScore(user.username, submittedLevel.levelIndex)
        userResults.append(UserResult(user.username, userScore))

    return userResults

def calculateUserScore(username, levelNum):
    return 55
