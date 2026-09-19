from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def before_scenario(context, scenario):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")

    context.driver = webdriver.Chrome(options=options)
    context.login_page = LoginPage(context.driver)
    context.inventory = InventoryPage(context.driver)


def after_scenario(context, scenario):
    context.driver.quit()
