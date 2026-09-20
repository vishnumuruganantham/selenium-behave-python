from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def before_scenario(context, scenario):

    context.driver = DriverFactory.get_driver()
    context.login_page = LoginPage(context.driver)
    context.inventory = InventoryPage(context.driver)


def after_scenario(context, scenario):
    context.driver.quit()
