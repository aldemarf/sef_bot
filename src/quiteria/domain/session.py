from datetime import datetime


class Session:
    SESSIONS = dict()

    def __init__(self, id=None, user=None, lastAcess=None, isLogged=False):
        self.id = id
        self.user = user
        self.lastAcess = lastAcess
        self.isLogged = isLogged

    @classmethod
    def setSession(cls, telegramID=None):
        session = Session()
        cls.SESSIONS[telegramID] = session

    @classmethod
    def startSession(cls, telegramID, user):
        session = cls.SESSIONS[telegramID]
        session.lastAcess = datetime.now()
        session.user = user

    @classmethod
    def endSession(cls, telegramID):
        if telegramID in cls.SESSIONS:
            del cls.SESSIONS[telegramID]
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

