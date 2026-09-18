from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support.ui import Select


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

driver.find_element(By.XPATH, "//button[text()='Delete']").click()
driver.get(base_url)
driver.find_element(By.XPATH, "//a[text()='Dropdown']").click()

# Select
dropdown = Select(driver.find_element(By.ID, "dropdown"))
dropdown.select_by_value("1")
dropdown.select_by_index(2)
dropdown.select_by_visible_text("Option 1")

print(f"Total options = {len(dropdown.options)}")
print(f"Selected option = {dropdown.first_selected_option.text}")
all_option_texts = [option.text for option in dropdown.options]
print(f"All texts of available options = {all_option_texts}")

try:
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.XPATH, "summa"))
    )
except (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
) as error:
    print(
        f"Just passing time after catching {error.__class__.__name__} exception"
    )  # It catches timeout exception
