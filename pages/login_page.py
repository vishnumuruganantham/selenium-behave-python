from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.config_reader import ConfigReader


class LoginPage(BasePage):

    user_name = (By.ID, "user-name")
    pass_word = (By.XPATH, "//input[@data-test='password']")
    submit_btn = (By.CSS_SELECTOR, "#login-button")
    error = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, env="prod", timeout=15):
        super().__init__(driver, timeout)
        self.url = ConfigReader().get_base_url(env)

    def is_loaded(self):
        return self.is_visible(self.user_name)

    def open_login_page(self):
        self.open(self.url)
        return self

    def login(self, user, password):
        self.type(self.user_name, user)
        self.type(self.pass_word, password)
        self.click(self.submit_btn)
        return self

    def error_message(self):
        return self.text(self.error)
