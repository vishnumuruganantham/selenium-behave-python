import json
from pathlib import Path


class DataReader:
    _data = None
    _data_path = Path(__file__).resolve().parent.parent / "test_data" / "users.json"

    @classmethod
    def _load(cls):
        if cls._data is None:  # read the file only once
            with open(cls._data_path) as f:
                cls._data = json.load(f)
        return cls._data

    @staticmethod
    def get_user(user_type):
        return DataReader._load()[user_type]

    @staticmethod
    def get():
        return DataReader._load()
