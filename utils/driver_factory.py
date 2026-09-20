from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:

    @staticmethod
    def get_driver(browser="chrome"):
        if browser == "chrome":
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            return webdriver.Chrome(options=options)
        elif browser == "firefox":
            return webdriver.Firefox()
        elif browser == "edge":
            return webdriver.Edge()
        raise ValueError(f"Unsupported browser: {browser}")
