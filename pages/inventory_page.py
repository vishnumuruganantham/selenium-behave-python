from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging


class InventoryPage(BasePage):

    product_title = (By.CSS_SELECTOR, "[data-test='title']")
    all_add_to_cart_buttons = (By.CSS_SELECTOR, "[data-test^='add-to-cart-']")
    all_item_price = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    total_item_count = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def is_loaded(self):
        return self.is_visible(self.product_title)

    def select_products(self):
        all_add_to_cart_buttons = self.multiple_elements(self.all_add_to_cart_buttons)
        for button in all_add_to_cart_buttons:
            self.click(button)
        cart_count = int(self.text(self.total_item_count))
        logging.info(f"{len(all_add_to_cart_buttons)} add to cart buttons clicked")
        logging.info(f"{cart_count} number of items added to cart")
        return len(all_add_to_cart_buttons) == cart_count

    def calculate_sum_of_all_prices(self):
        all_prices = self.multiple_elements(self.all_item_price)
        total = 0.0
        for price in all_prices:
            cost = float(price.text.replace("$", ""))
            total += cost
        return total
