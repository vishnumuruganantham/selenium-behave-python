import parse
from behave import given, when, then, register_type


@parse.with_pattern(r".*")
def parse_text(text):
    return text


register_type(Text=parse_text)


@given("the login page is open")
def step_open(context):
    context.login_page.open_login_page()


@when('the user logs in as "{user:Text}" with password "{pwd:Text}"')
def login(context, user, pwd):
    context.login_page.login(user, pwd)


@then('an error "{message}" is shown')
def step_inventory(context, message):
    assert message in context.login_page.error_message(), "Error message is not seen"
