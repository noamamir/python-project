from models.registeredLevel import RegisteredLevel


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.levelsPaths: RegisteredLevel

