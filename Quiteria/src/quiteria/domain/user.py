class User:
    def __init__(self, uid=None, telegram_id=None, name=None,
                 email=None, lab=None, role=None, active=False):
        self.id = uid
        self.telegramID = telegram_id
        self.name = name
        self.email = email
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

    def from_dict(self, dic):
        self.id = dic['id']
        self.telegramID = dic['telegramID']
        self.name = dic['id']
        self.email = dic['id']
        self.lab = dic['id']
        self.role = dic['id']
        self.active = dic['id']
