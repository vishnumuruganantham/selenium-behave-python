from behave import then


@then("the user navigates to checkout page")
def navigate_to_checkout_page(context):
    # Captured here, before navigating away, so the later subtotal-match
    # step (checkout_steps.py) has a baseline from the inventory page
    # itself rather than depending on the checkout page reusing the same
    # price locator.
    assert context.cart_page.is_loaded(), "Cart page is not loaded"
    context.cart_page.navigate_to_checkout_page()
