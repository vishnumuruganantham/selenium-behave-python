from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage(ABC):
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        return self

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        el.clear()
        el.send_keys(text)

    def text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(locator)
            ).is_displayed()
        except TimeoutException:
            return False

    def multiple_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    @abstractmethod
    def is_loaded(self):
        """Each page must define its own loading verification logic."""
        pass
