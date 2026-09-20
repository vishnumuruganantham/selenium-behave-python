import json


class DataReader:
    _data = None

    @classmethod
    def _load(cls):
        if cls._data is None:  # read the file only once
            with open("test_data/users.json") as f:
                cls._data = json.load(f)
        return cls._data

    @staticmethod
    def get_user(user_type):
        return DataReader._load()[user_type]

    @staticmethod
    def get():
        return DataReader._load()
