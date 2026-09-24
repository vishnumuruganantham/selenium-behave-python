from behave import then


@then("the user enters information on checkout and clicks continue")
def enter_checkout_information(context):
    assert context.checkout_page.is_loaded(), "Checkout page is not loaded"
    context.checkout_page.input_checkout_info()


@then("the subtotal price should match with the prices displayed in inventory page")
def assert_subtotal_matches_inventory(context):
    assert (
        context.expected_subtotal == context.checkout_page.subtotal_value()
    ), "Mismatch in sub total amounts present in inventory page and checkout page"


@then("the user submits the order")
def submit_order(context):
    context.checkout_page.submit_order()


@then("the user downloads the receipt")
def assert_order_placed_and_download_receipt(context):
    assert (
        context.checkout_page.checks_successful_order_placement()
        == "Thank you for your order!"
    )
    downloaded_file = context.checkout_page.download_receipt()
    assert downloaded_file is not None, "Receipt PDF was not downloaded within 10s"
