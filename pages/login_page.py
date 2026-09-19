from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    user_name = (By.ID, "user-name")
    pass_word = (By.XPATH, "//input[@data-test='password']")
    submit_btn = (By.CSS_SELECTOR, "#login-button")
    error = (By.CSS_SELECTOR, "[data-test='error']")

    def is_loaded(self):
        return self.is_visible(self.user_name)

    def open_login_page(self):
        self.open(self.URL)
        return self

    def login(self, user, password):
        self.type(self.user_name, user)
        self.type(self.pass_word, password)
        self.click(self.submit_btn)

    def error_message(self):
        return self.text(self.error)
