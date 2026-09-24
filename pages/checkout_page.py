from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from utils.data_reader import DataReader
from utils.driver_factory import DOWNLOAD_DIR
import logging
import os
import time


class CheckoutPage(BasePage):

    title = (By.CSS_SELECTOR, ".title")
    first_name = (By.CSS_SELECTOR, "#first-name")
    last_name = (By.CSS_SELECTOR, "#last-name")
    zip_code = (By.CSS_SELECTOR, "#postal-code")
    btn_continue = (By.ID, "continue")
    sub_total = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    btn_finish = (By.XPATH, "//button[@data-test='finish']")
    success_msg = (By.XPATH, "//h2[@data-test='complete-header']")
    btn_download_receipt = (By.XPATH, "//button[@data-test='generate-pdf-order']")

    def __init__(self, driver, timeout=15):
        super().__init__(driver, timeout)
        self.checkout_info = DataReader.get_user("checkout_info")

    def is_loaded(self):
        return self.text(self.title) == "Checkout: Your Information"

    def input_checkout_info(self):
        self.enter_text(self.first_name, self.checkout_info["first_name"])
        self.enter_text(self.last_name, self.checkout_info["last_name"])
        self.enter_text(self.zip_code, self.checkout_info["postal_code"])
        self.click(self.btn_continue)

    def subtotal_value(self):
        subtotal = float(self.text(self.sub_total).replace("Item total: $", ""))
        logging.info(f"{subtotal} is the subtotal in Checkout page before adding tax")
        return subtotal

    def submit_order(self):
        self.click(self.btn_finish)

    def checks_successful_order_placement(self):
        return self.text(self.success_msg)

    def download_receipt(self):
        existing_files = set(os.listdir(DOWNLOAD_DIR)) if DOWNLOAD_DIR.exists() else set()
        self.click(self.btn_download_receipt)

        deadline = time.time() + 10
        while time.time() < deadline:
            new_files = set(os.listdir(DOWNLOAD_DIR)) - existing_files
            pdfs = [f for f in new_files if f.lower().endswith(".pdf")]
            still_downloading = any(f.endswith(".crdownload") for f in new_files)
            if pdfs and not still_downloading:
                downloaded_file = DOWNLOAD_DIR / pdfs[0]
                logging.info(f"Receipt downloaded to {downloaded_file}")
                return downloaded_file
            time.sleep(0.5)

        return None
