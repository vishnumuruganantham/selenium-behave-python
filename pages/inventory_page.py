from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import logging


class InventoryPage(BasePage):

    product_title = (By.CSS_SELECTOR, "[data-test='title']")
    all_add_to_cart_buttons = (By.CSS_SELECTOR, "[data-test^='add-to-cart-']")
    all_item_price = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    total_item_count = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    cart_button = (By.CSS_SELECTOR, "#shopping_cart_container")

    def is_loaded(self):
        return self.is_visible(self.product_title)

    def select_products(self):
        # Capture each button's own unique data-test value upfront, then
        # click each one via its own unique locator, instead of reusing one
        # ambiguous "first match" locator across the whole loop. This avoids
        # any dependence on click/render ordering for a specific button.
        # (The actual flakiness we hit turned out to be Chrome's password-
        # leak-warning dialog eating clicks — see driver_factory.py — but
        # this is still the more correct pattern regardless.)
        product_ids = [
            el.get_attribute("data-test")
            for el in self.multiple_elements(self.all_add_to_cart_buttons)
        ]
        for product_id in product_ids:
            self.click((By.CSS_SELECTOR, f"[data-test='{product_id}']"))

        total_products = len(product_ids)
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

    def navigate_to_cart_page(self):
        self.click(self.cart_button)
