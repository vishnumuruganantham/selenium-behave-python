from behave import when, then
from pages.inventory_page import InventoryPage


@then("the inventory page is displayed")
def step_inventory(context):
    assert context.inventory.is_loaded(), "Inventory page did not load"


@then("the user should be able to add products to cart")
def step_open(context):
    assert context.inventory.select_products(), "Unable to select"
