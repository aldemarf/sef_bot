class Maintenance:
    def __init__(self, mid=None, telegram_id=None, local=None,
                 date=None, time=None, approved=None, done=False):
        self.id = mid
        self.telegramID = telegram_id
        self.local = local
        self.date = date
        self.time = time
        self.approved = approved
        self.done = done

    def __str__(self) -> str:
        return 'Order ID : {}\n User ID : {}\nLocal : {}\n' \
               'Date : {}\nTime : {}\nDone : {}\n'\
            .format(self.id, self.local,
                    self.date, self.time,
                    self.approved, self.done
                    )
