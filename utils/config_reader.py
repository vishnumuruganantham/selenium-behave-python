import configparser


class ConfigReader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.parser = configparser.ConfigParser()
            cls._instance.parser.read("config/config.ini")
        return cls._instance

    def get(self, section, key):
        return self.parser.get(section, key)
