#

import time


class HistoryModel(object):
    def __init__(self, date=None):
        self.date = date

    def get_prepare_date(self):
        result = time.strptime(self.date, "%Y-%m-%dT%H:%M:%S")
        return result
