from datetime import datetime


class TransDate:
    def __init__(self, date):
        self.date = date

    def get_today_min(self):
        today_min = datetime.combine(self.date, datetime.min.time())
        return today_min

    def get_today_max(self):
        today_max = datetime.combine(self.date, datetime.max.time())
        return today_max
