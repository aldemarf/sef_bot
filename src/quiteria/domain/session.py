import logging
from datetime import datetime


class Session:
    sessions = dict()

    def __init__(self, uid=None, user=None,
                 last_acess=None, logged=False, attempts=0, is_empty=True):
        self.id = uid
        self.user = user
        self.lastAcess = last_acess
        self.logged = logged
        self.loginAttempts = attempts
        self.isEmpty = is_empty

    @classmethod
    def startSession(cls, telegram_id):
        session = cls.sessions[telegram_id]
        session.lastAcess = datetime.now()

    @classmethod
    def endSession(cls, telegram_id):
        if telegram_id in cls.sessions:
            del cls.sessions[telegram_id]
        else:
            return logging.error('Sessão inexistente')

    @classmethod
    def getSession(cls, telegram_id):
        sessions = cls.sessions
        if telegram_id not in sessions:
            sessions[telegram_id] = Session()

        return sessions[telegram_id]

    @staticmethod
    def loadSessions():
        # TODO: Load from SQLite
        pass

    @staticmethod
    def saveSessions():
        # TODO: Persist sessions on SQLite

        pass
