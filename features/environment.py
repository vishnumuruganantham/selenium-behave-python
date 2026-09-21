from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
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
        handlers=[logging.FileHandler("reports/test_run.log"), logging.StreamHandler()],
    )
    logging.info("Test run started")


def before_scenario(context, scenario):
    browser = context.config.userdata.get("browser", "chrome")
    context.driver = DriverFactory.get_driver(browser)
    context.login_page = LoginPage(context.driver)
    context.inventory = InventoryPage(context.driver)
    logging.info(f"Starting scenario: {scenario.name}")


def after_step(context, step):
    if step.status == "failed":
        # This attaches perfectly to Allure regardless of characters
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=step.name,
            attachment_type=allure.attachment_type.PNG,
        )

        # Local backup path
        folder = "screenshots"
        if not os.path.exists(folder):
            os.makedirs(folder)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Strip spaces and illegal characters out for the local filename
        safe_step_name = "".join(
            c for c in step.name if c.isalnum() or c in (" ", "_")
        ).replace(" ", "_")
        context.driver.save_screenshot(f"screenshots/{timestamp}_{safe_step_name}.png")


def after_scenario(context, scenario):
    try:  # Wrapped in try/except so a cleanup error never masks the real reason the test failed
        logging.info(f"Finished scenario: {scenario.name} — {scenario.status}")
        context.driver.quit()
    except Exception:
        pass
