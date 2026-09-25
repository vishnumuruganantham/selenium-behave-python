from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.config_reader import ConfigReader
from datetime import datetime
import os
import allure
import logging


def before_all(context):
    context.config_data = ConfigReader()

    # Make sure the reports folder exists before the FileHandler tries to write into it
    os.makedirs("reports", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                "reports/test_run.log", encoding="utf-8"
            ),  # ← add encoding
            logging.StreamHandler(),
        ],
    )
    logging.info("Test run started")


def before_scenario(context, scenario):
    browser = context.config.userdata.get("browser", "chrome")
    env = context.config.userdata.get("env", "prod")
    headless = context.config.userdata.getbool("headless", False)
    context.driver = DriverFactory.get_driver(browser, headless)
    context.login_page = LoginPage(context.driver, env)
    context.inventory_page = InventoryPage(context.driver)
    context.cart_page = CartPage(context.driver)
    context.checkout_page = CheckoutPage(context.driver)
    logging.info(f"Starting scenario: {scenario.name}")


def after_step(context, step):
    if step.status != "failed":
        return
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    try:
        png = driver.get_screenshot_as_png()
    except Exception:
        logging.exception(f"Could not capture screenshot for failed step: {step.name}")
        return
    allure.attach(png, name=step.name, attachment_type=allure.attachment_type.PNG)

    # Local backup path
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_step_name = "".join(
        c for c in step.name if c.isalnum() or c in (" ", "_")
    ).replace(" ", "_")

    try:
        with open(f"screenshots/{timestamp}_{safe_step_name}.png", "wb") as f:
            f.write(png)
    except OSError:
        logging.exception("Could not save local screenshot backup")


def after_scenario(context, scenario):
    logging.info(f"Finished scenario: {scenario.name} — {scenario.status}")

    driver = getattr(context, "driver", None)
    if driver is None:
        return

    try:
        driver.quit()
    except Exception:
        logging.exception(
            f"Failed to quit driver cleanly for scenario: {scenario.name}"
        )
