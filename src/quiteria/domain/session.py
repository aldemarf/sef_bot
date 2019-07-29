from datetime import datetime


class Session:
    sessions = dict()

    def __init__(self, uid=None, user=None,
                 last_acess=None, logged=False, attempts=0):
        self.id = uid
        self.user = user
        self.lastAcess = last_acess
        self.logged = logged
        self.loginAttempts = attempts

    @classmethod
    def setSession(cls, telegram_id):
        session = Session()
        cls.sessions[telegram_id] = session

    @classmethod
    def startSession(cls, telegram_id, user):
        session = cls.sessions[telegram_id]
        session.lastAcess = datetime.now()
        session.user = user

    @classmethod
    def endSession(cls, telegram_id):
        if telegram_id in cls.sessions:
            del cls.sessions[telegram_id]
        else:
            raise KeyError('Sessão inexistente')

    @staticmethod
    def loadSessions():
        # TODO: Load from SQLite
        pass

    @staticmethod
    def saveSessions():
        # TODO: Persist sessions on SQLite

        pass
