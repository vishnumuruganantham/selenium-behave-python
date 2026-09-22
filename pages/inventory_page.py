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
        total_products = len(self.multiple_elements(self.all_add_to_cart_buttons))
        for _ in range(total_products):
            # Re-locates fresh each call. Clicking flips a button's data-test
            # from add-to-cart-* to remove-*, so the same locator always
            # matches the next remaining "Add to cart" button.
            self.click(self.all_add_to_cart_buttons)
        cart_count = int(self.text(self.total_item_count))
        logging.info(f"{total_products} add to cart buttons clicked")
        logging.info(f"{cart_count} number of items added to cart")
        return total_products, cart_count

    def calculate_sum_of_all_prices(self):
        all_prices = self.multiple_elements(self.all_item_price)
        total = 0.0
        for price in all_prices:
            cost = float(price.text.replace("$", ""))
            total += cost
        return total
