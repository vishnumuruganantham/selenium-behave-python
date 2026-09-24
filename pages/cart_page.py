from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CartPage(BasePage):

    title = (By.CSS_SELECTOR, "[data-test='title']")
    btn_checkout = (By.CSS_SELECTOR, "[data-test='checkout']")

    def is_loaded(self):
        return self.text(self.title) == "Your Cart"

    def navigate_to_checkout_page(self):
        self.click(self.btn_checkout)
