class User:
    def __init__(self, uid=None, telegram_id=None, name=None,
                 email=None, password=None, lab=None, role=None,
                 active=False):
        self.id = uid
        self.telegramID = telegram_id
        self.name = name
        self.email = email
        self.password = password
        self.lab = lab
        self.role = role
        self.active = active

    def __str__(self) -> str:
        return 'User ID : {}\n Name : {}\nEmail : {}\n' \
               'Lab : {}\nRole : {}\nStatus : {}\n'\
            .format(self.id, self.name,
                    self.email, self.lab,
                    self.role, self.active
                    )

    def fromProxy(self, proxy):
        from quiteria.persistence.sqlite import SQLiteDB

        self.id = proxy[SQLiteDB.C_USER_ID]
        self.telegramID = proxy[SQLiteDB.C_USER_TG_ID]
        self.name = proxy[SQLiteDB.C_USER_NAME]
        self.email = proxy[SQLiteDB.C_USER_EMAIL]
        self.password = proxy[SQLiteDB.C_USER_PWD]
        self.lab = proxy[SQLiteDB.C_USER_LAB]
        self.role = proxy[SQLiteDB.C_USER_ROLE]
        self.active = proxy[SQLiteDB.C_USER_ACTIVE]
