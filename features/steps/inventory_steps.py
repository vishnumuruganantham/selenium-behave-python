from behave import then


@then("the inventory page is displayed")
def assert_inventory_page_loaded(context):
    assert context.inventory_page.is_loaded(), "Inventory page did not load"


@then("the user should be able to add products to cart")
def assert_all_products_added_to_cart(context):
    total, added = context.inventory_page.select_products()
    assert (
        total == added
    ), f"Expected {total} items added to cart, but cart shows {added}"
