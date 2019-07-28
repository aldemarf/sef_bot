from datetime import datetime


class Session:
    sessions = dict()

    def __init__(self, id=None, user=None, lastAcess=None, logged=False):
        self.id = id
        self.user = user
        self.lastAcess = lastAcess
        self.logged = logged

    @classmethod
    def setSession(cls, telegramID):
        session = Session()
        cls.sessions[telegramID] = session

    @classmethod
    def startSession(cls, telegramID, user):
        session = cls.sessions[telegramID]
        session.lastAcess = datetime.now()
        session.user = user

    @classmethod
    def endSession(cls, telegramID):
        if telegramID in cls.sessions:
            del cls.sessions[telegramID]
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

