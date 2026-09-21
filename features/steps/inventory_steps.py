from behave import then


@then("the inventory page is displayed")
def step_inventory(context):
    assert context.inventory_page.is_loaded(), "Inventory page did not load"


@then("the user should be able to add products to cart")
def step_open(context):
    assert context.inventory_page.select_products(), "Unable to select"
