from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    NoSuchFrameException,
)
import time
from utils.data_reader import DataReader

import os
from dotenv import load_dotenv


def create_driver():

    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless=new")

    d = webdriver.Chrome(options=options)
    return d


driver = create_driver()
base_url = "https://the-internet.herokuapp.com"
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
print(f"All texts = {all_option_texts}")

try:
    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.XPATH, "summa"))
    )
except (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
) as error:
    print(
        f"Safely caught expected exception:  {error.__class__.__name__}"
    )  # It catches timeout exception

driver.get(f"{base_url}/javascript_alerts")

# Alerts

driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
alert = driver.switch_to.alert
message_alert_1 = alert.text
print(f"First alert's message: {message_alert_1}")
alert.accept()

driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
alert = driver.switch_to.alert
message_alert_2 = alert.text
print(f"Second alert's message: {message_alert_2}")
alert.dismiss()

driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
alert = driver.switch_to.alert
message_alert_3 = alert.text
print(f"Third alert's message: {message_alert_3}")
text_to_send = "Hi Vanakams"
alert.send_keys(text_to_send)
alert.accept()
result = driver.find_element(By.XPATH, "//p[@id='result']").text
print(result)

if text_to_send in result:
    print("Nee sadhichuta da dai! (Text verification passed)")

driver.get(f"{base_url}/hovers")

# Actions
actions = ActionChains(driver)

element_1 = driver.find_element(
    By.XPATH, "//h5[text()='name: user1']/ancestor::div[@class='figure']"
)

# Hover : Only the element which is hovered's text is shown
actions.move_to_element(element_1).perform()
print(
    f"Is user 3 seen: {driver.find_element(By.XPATH, "//h5[text()='name: user3']").is_displayed()}"
)
print(
    f"Is user 1 seen?: {driver.find_element(By.XPATH, "//h5[text()='name: user1']").is_displayed()}"
)

# Context click
driver.get(f"{base_url}/context_menu")
actions.context_click(driver.find_element(By.ID, "hot-spot")).perform()
driver.switch_to.alert.accept()
actions.key_down(Keys.ALT).send_keys(Keys.ARROW_LEFT).key_up(Keys.ALT).perform()
actions.send_keys(Keys.ESCAPE).perform()
# Tried to get rid of context dropdown, no luck.

# Drag and drop
driver.get(f"{base_url}/drag_and_drop")
element_a = driver.find_element(By.ID, "column-a")
element_b = driver.find_element(By.ID, "column-b")
actions.click_and_hold(element_a).move_to_element(element_b).release().perform()
# or
actions.drag_and_drop(element_a, element_b).perform()

driver.get(f"{base_url}/nested_frames")
# Frames

# Switch to frame with name "frame-top"
driver.switch_to.frame("frame-top")

# Navigates next inside another frame which has name "frame-left"
driver.switch_to.frame("frame-left")

driver.switch_to.parent_frame()  # Switches one frame up
driver.switch_to.default_content()  # Switches to page level

# Using webdriver wait to switch to frame
WebDriverWait(driver, 20).until(
    EC.frame_to_be_available_and_switch_to_it("frame-bottom")
)
try:
    driver.switch_to.frame("frame-left")
except NoSuchFrameException:
    print(
        "Threw 'NoSuchFrameExceptionexception' as we are not in default content to switch to this frame"
    )

driver.get(f"{base_url}/windows")
# Window Handles

main_handle = driver.current_window_handle

link = driver.find_element(By.LINK_TEXT, "Click Here")
link.click()

print(f"Number of windows open = {len(driver.window_handles)}")

for handle in driver.window_handles:
    if handle != main_handle:
        driver.switch_to.window(handle)
        driver.close()

driver.switch_to.window(main_handle)
driver.switch_to.new_window("tab")
driver.close()  # Closes last opened tab alone
driver.switch_to.window(main_handle)
driver.switch_to.new_window("window")
driver.close()  # Closes last opened single tab window. driver.quit() will close all windows and tabs
driver.switch_to.window(main_handle)

# Test Data: Reading through data_reader

# Fetching particular user
valid_user = DataReader.get_user("valid_user")
for key, value in valid_user.items():
    print(key, value)

all_users = DataReader.get()

# Loop through and print the users
print("--- Printing User Profiles ---")
for profile_name, details in all_users.items():
    print(f"\nProfile: {profile_name}")
    print(f"  Username: {details.get('username')}")
    print(f"  Password: {details.get('password')}")

    # Check if it has a dashboard or an error message expected
    if "expected_dashboard" in details:
        print(f"  Expected: {details['expected_dashboard']}")
    elif "expected_error" in details:
        print(f"  Expected: {details['expected_error']}")

# Reading from .env file
load_dotenv()  # reads .env and loads its keys into environment variables

username = os.getenv("TEST_USERNAME")
password = os.getenv("TEST_PASSWORD")
bank_account = os.getenv("TEST_BANK_ACCOUNT_NUMBER")
api_key = os.getenv("API_KEY")

print(f"\nReading from .env file kept locally: {bank_account}")  

time.sleep(5)
