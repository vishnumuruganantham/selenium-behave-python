from behave import then


@then("the user navigates to checkout page")
def step_impl(context):
    context.cart_page.navigate_to_checkout_page()
