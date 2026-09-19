from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class InventoryPage(BasePage):

    product_title = (By.CSS_SELECTOR, "[data-test='title']")

    def is_loaded(self):
        return self.is_visible(self.product_title)
