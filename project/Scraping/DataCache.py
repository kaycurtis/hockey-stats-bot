import datetime

class DataCache:

    def __init__(self, html):
        self.date_created = datetime.datetime.now()
        self.html = html
        self.player_statistics = {}

    def is_expired(self):
        date = datetime.datetime.now()
        if date.date() != self.date_created.date():
            return True
        else:
            return False