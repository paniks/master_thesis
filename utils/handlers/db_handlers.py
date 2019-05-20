import pandas as pd

from base import BaseDBHandler


class LocalDBHandler(BaseDBHandler):
    def __init__(self):
        super().__init__()
        self.db: pd.DataFrame = None
        self.path: str = ''

    def init_db(self, path: str):
        self.path = path
        self.db = pd.read_pickle(path)

    def insert(self, data: dict):
        tmp_data = pd.Series(data)
        self.validate(tmp_data)
        self.db = self.db.append(tmp_data, ignore_index=True)
        self.db.to_pickle(self.path)

    def validate(self, data: pd.Series):
        if not (data.keys().values == self.db.keys().values).all():
            raise KeyError('Keys from query and db are different')
        if not self.db[self.db['username'] == data['username']].empty:
            raise AssertionError('There is user with same name in db')

    def get(self, username) -> dict:
        idx = self.db[self.db['username'] == username].index.item()
        record = self.db.loc[idx].to_dict()
        return record
