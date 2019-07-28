from sqlalchemy import (MetaData, create_engine, Table,
                        Column, String, Integer, Boolean, Date)

from quiteria.domain.user import User


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
    C_USER_ACTIVE = 'isActive'

    # ROOM COLUMNS
    C_ROOM_ID = 'id'

    # MAINTENANCE COLUMNS
    C_MNTNNC_ID = 'id'

    # ## DATABASE PATHS ###
    DB_MEMORY = 'sqlite:///:memory:'
    DB_FILE = 'sqlite:///quiteria.sqlite'
    DB_PATH = DB_FILE


    @staticmethod
    def create_sessions_table(engine):
        metadata = MetaData()
        Table(
            SQLiteDB.SESSIONS_TABLE, metadata,
            Column(SQLiteDB.C_SESSION_ID, Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False),
            Column(SQLiteDB.C_SESSION_USER_ID, Integer,
                   nullable=False,
                   unique=True),
            Column(SQLiteDB.C_SESSION_LAST_ACCESS, Date,
                   nullable=False),
            Column(SQLiteDB.C_SESSION_ISLOGGED, Boolean,
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
                   autoincrement=True,
                   nullable=False),
            Column(SQLiteDB.C_USER_TG_ID, Integer,
                   nullable=False,
                   unique=True),
            Column(SQLiteDB.C_USER_NAME, String(150),
                   nullable=False),
            Column(SQLiteDB.C_USER_EMAIL, String(70),
                   nullable=False,
                   unique=True),
            Column(SQLiteDB.C_USER_PWD, String(16),
                   nullable=False),
            Column(SQLiteDB.C_USER_LAB, String(50)),
            Column(SQLiteDB.C_USER_ROLE, String(50)),
            Column(SQLiteDB.C_USER_ACTIVE, Boolean,
                   nullable=False,
                   default=False)
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

    @staticmethod
    def create_tables():
        engine = create_engine(SQLiteDB.DB_PATH, echo=True)
        SQLiteDB.create_sessions_table(engine)
        SQLiteDB.create_user_table(engine)
        SQLiteDB.create_room_table(engine)
        SQLiteDB.create_maintenance_table(engine)

    @staticmethod
    def drop_user_table(engine):
        metadata = MetaData()
        Table(SQLiteDB.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @staticmethod
    def drop_maintenance_table(engine):
        metadata = MetaData()
        Table(SQLiteDB.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @staticmethod
    def drop_room_table(engine):
        metadata = MetaData()
        Table(SQLiteDB.USER_TABLE, metadata).drop(engine, checkfirst=True)

    @staticmethod
    def drop_tables():
        engine = create_engine(SQLiteDB.DB_PATH, echo=True)
        SQLiteDB.drop_user_table(engine)
        SQLiteDB.drop_room_table(engine)
        SQLiteDB.drop_maintenance_table(engine)


#########################################################


class UserDAO:

    def __init__(self):
        self.metadata = MetaData()
        self.engine = create_engine(SQLiteDB.DB_PATH, echo=True)

    def insert_user(self, entries):
        values = []
        users = entries

        if not isinstance(entries, list):
            users = [entries]
        else:
            for item in users:
                values.append(dict(
                    name=item.name,
                    email=item.email,
                    lab=item.lab,
                    role=item.role,
                    active=item.active
                ))

        user_table = Table(SQLiteDB.USER_TABLE, self.metadata,
                           autoload=True,
                           autoload_with=self.engine)
        result = user_table.insert().values(users)

        return result.inserted_primary_key

    def get_user(self, telegram_id):
        user = Table(SQLiteDB.USER_TABLE, self.metadata,
                     autoload=True,
                     autoload_with=self.engine)

        with self.engine.connect() as connection:
            sel = user.select()
            sel = sel.where(user.c.telegram_id == telegram_id)
            result = connection.execute(sel).fetchall()

        return result

    @staticmethod
    def create_user(data):
        # TODO :
        # user = User()
        # if data is None:
        #     raise RuntimeError("Dados invalidos")
        # else:
        #     user.from_dict(data)
        # return user
        pass


class RoomDAO:
    pass


class MaintenanceDAO:
    pass
