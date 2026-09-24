from behave import then
import logging


@then("the inventory page is displayed")
def assert_inventory_page_loaded(context):
    assert context.inventory_page.is_loaded(), "Inventory page did not load"


@then("the user should be able to add products to cart")
def assert_all_products_added_to_cart(context):
    total, added = context.inventory_page.select_products()
    assert (
        total == added
    ), f"Expected {total} items added to cart, but cart shows {added}"


@then("the user should be able to navigate to cart page")
def navigate_to_cart_page(context):
    context.expected_subtotal = context.inventory_page.calculate_sum_of_all_prices()
    context.inventory_page.navigate_to_cart_page()
    logging.info(
        f"{context.expected_subtotal} is the sum of all prices of products in inventory page"
    )
