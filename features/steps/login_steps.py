from behave import given, when, then, use_step_matcher
from pages.login_page import LoginPage


@given("the login page is open")
def step_open(context):
    context.login = LoginPage(context.driver).open_login_page()


@when('the user logs in as "{user}" with password "{pwd}"')
def login(context, user, pwd):
    if user == "empty":
        context.inventory_page = context.login_page.login(None, pwd)
    else:
        context.inventory_page = context.login_page.login(user, pwd)


@then("the inventory page is displayed")
def step_inventory(context):
    assert context.inventory.is_loaded(), "Inventory page did not load"


@then('an error "{message}" is shown')
def step_inventory(context, message):
    assert message in context.login.error_message(), "Error message is not seen"
