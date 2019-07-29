from sqlalchemy import (MetaData, create_engine, Table,
                        Column, String, Integer, Boolean, Date)


class SQLiteDB:
    # TABLES
    USER_TABLE = 'users'
    USER_SESSION_TABLE = 'users_sessions'
    ROOM_SCH_TABLE = 'room_schd'
    MAINTENANCE_SCH_TABLE = 'maintenance_schd'
    SESSIONS_TABLE = 'sessions'

    # SESSION COLUMNS
    C_SESSION_ID = 'id'
    C_SESSION_USER_ID = 'user_id'
    C_SESSION_LAST_ACCESS = 'last_acess'
    C_SESSION_ISLOGGED = 'is_logged'

    # USER COLUMNS
    C_USER_ID = 'id'
    C_USER_TG_ID = 'telegram_id'
    C_USER_NAME = 'name'
    C_USER_EMAIL = 'email'
    C_USER_PWD = 'pwd'
    C_USER_LAB = 'lab'
    C_USER_ROLE = 'role'
    C_USER_ACTIVE = 'active'

    # ROOM COLUMNS
    C_ROOM_ID = 'id'

    # MAINTENANCE COLUMNS
    C_MNTNNC_ID = 'id'

    # ## DATABASE PATHS ###
    DB_MEMORY = 'sqlite:///:memory:'
    DB_FILE = 'sqlite:///quiteria.sqlite'
    DB_PATH = DB_FILE

    @classmethod
    def create_sessions_table(cls, engine):
        metadata = MetaData()
        Table(
            cls.SESSIONS_TABLE, metadata,
            Column(cls.C_SESSION_ID, Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False),
            Column(cls.C_SESSION_USER_ID, Integer,
                   nullable=False,
                   unique=True),
            Column(cls.C_SESSION_LAST_ACCESS, Date,
                   nullable=False),
            Column(cls.C_SESSION_ISLOGGED, Boolean,
                   nullable=False,
                   unique=True)
        ).create(engine, checkfirst=True)

    @staticmethod
    def create_user_table(engine):
        metadata = MetaData()
        Table(
            SQLiteDB.USER_TABLE, metadata,
            Column(SQLiteDB.C_USER_ID, Integer,
                   primary_key=True,
                   autoincrement=True),
            Column(SQLiteDB.C_USER_TG_ID, Integer,
                   nullable=False,
                   unique=True),
            Column(SQLiteDB.C_USER_NAME, String(150),
                   nullable=False),
            Column(SQLiteDB.C_USER_EMAIL, String(70),
                   nullable=True,
                   unique=True),
            Column(SQLiteDB.C_USER_PWD, String(16),
                   nullable=False),
            Column(SQLiteDB.C_USER_LAB, String(50)),
            Column(SQLiteDB.C_USER_ROLE, String(50)),
            Column(SQLiteDB.C_USER_ACTIVE, Boolean,
                   nullable=False)
        ).create(engine, checkfirst=True)

    @staticmethod
    def create_maintenance_table(engine):
        metadata = MetaData()
        Table(
            SQLiteDB.MAINTENANCE_SCH_TABLE, metadata,
            Column(SQLiteDB.C_MNTNNC_ID, Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
        ).create(engine, checkfirst=True)

    @staticmethod
    def create_room_table(engine):
        metadata = MetaData()
        Table(
            SQLiteDB.ROOM_SCH_TABLE, metadata,
            Column(SQLiteDB.C_ROOM_ID, Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
        ).create(engine, checkfirst=True)

    @classmethod
    def create_tables(cls):
        engine = create_engine(cls.DB_PATH, echo=True)
        cls.create_sessions_table(engine)
        cls.create_user_table(engine)
        cls.create_room_table(engine)
        cls.create_maintenance_table(engine)

    @classmethod
    def drop_user_table(cls, engine):
        metadata = MetaData()
        Table(cls.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @classmethod
    def drop_maintenance_table(cls, engine):
        metadata = MetaData()
        Table(cls.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @classmethod
    def drop_room_table(cls, engine):
        metadata = MetaData()
        Table(cls.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @classmethod
    def drop_tables(cls):
        engine = create_engine(cls.DB_PATH, echo=True)
        cls.drop_user_table(engine)
        cls.drop_room_table(engine)
        cls.drop_maintenance_table(engine)


#########################################################


class UserDAO:

    def __init__(self):
        self.metadata = MetaData()
        self.engine = create_engine(SQLiteDB.DB_PATH, echo=True)

    def insert_user(self, user):
        values = dict(
            telegram_id=user.telegramID,
            name=user.name,
            email=user.email,
            pwd=user.password,
            lab=user.lab,
            role=user.role,
            active=user.active)

        user_table = Table(SQLiteDB.USER_TABLE, self.metadata,
                           autoload=True,
                           autoload_with=self.engine)
        stmt = user_table.insert().values(values)

        with self.engine.connect() as connection:
            result = connection.execute(stmt)

        return result.inserted_primary_key

    def get_user(self, telegram_id):
        user = Table(SQLiteDB.USER_TABLE, self.metadata,
                     autoload=True,
                     autoload_with=self.engine)
        sel = user.select()
        sel = sel.where(user.c.telegram_id == telegram_id)

        with self.engine.connect() as connection:
            result = connection.execute(sel).fetchone()

        return self.createUser(result)

    @staticmethod
    def createUser(result):
        from quiteria.domain.user import User

        user = User()
        if result is None:
            raise RuntimeError("Dados invalidos")
        else:
            user.fromProxy(result)

        return user


class RoomDAO:
    pass


class MaintenanceDAO:
    pass
