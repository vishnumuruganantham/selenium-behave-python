import configparser
from pathlib import Path


class ConfigReader:
    _instance = None
    _config_path = Path(__file__).resolve().parent.parent / "config" / "config.ini"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.parser = configparser.ConfigParser()
            cls._instance.parser.read(cls._config_path)
        return cls._instance

    def get(self, section, key):
        return self.parser.get(section, key)

    def get_base_url(self, env):
        return self.get(env, "base_url")
