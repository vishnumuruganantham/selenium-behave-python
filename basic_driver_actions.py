from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


def create_driver():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    return driver


driver = create_driver()
base_url = "https://the-internet.herokuapp.com/"
driver.get(base_url)


# Meddling with URL, going to new url and coming back and forward
print(driver.current_url)
driver.refresh()
driver.get("https://google.com")
driver.get(base_url)

driver.back()
driver.forward()


# Waits

# Implicit wait
driver.implicitly_wait(0)  # Never use implicit wait

# Explicit wait
explicit_wait_for_element_and_click = (
    WebDriverWait(driver, 20)
    .until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Add/Remove Elements']")))
    .click()
)

# Fluent wait
fluent_wait_for_element_and_click = (
    WebDriverWait(
        driver,
        20,
        poll_frequency=0.8,
        ignored_exceptions=[StaleElementReferenceException],
    )
    .until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Add Element']")))
    .click()
)
