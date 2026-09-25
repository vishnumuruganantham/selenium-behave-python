from abc import ABC, abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class BasePage(ABC):
    def __init__(self, driver, timeout=15):
        self.driver = driver
        # By default WebDriverWait only ignores NoSuchElementException while
        # polling, so a StaleElementReferenceException (the element existed
        # a moment ago but got swapped out - e.g. mid page-transition) is
        # raised immediately instead of being retried. Also ignore it here
        # so every wait below tolerates the DOM changing under it, instead
        # of failing on a transient race.
        self.wait = WebDriverWait(
            driver, timeout, ignored_exceptions=[StaleElementReferenceException]
        )

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
