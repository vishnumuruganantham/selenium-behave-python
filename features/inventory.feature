@smoke
Feature: Inventory page

	Scenario: Whether all products are able to be added to cart
		Given the login page is open
		When the user logs in as "standard_user" with password "secret_sauce"
		Then the inventory page is displayed
		And  the user should be able to add products to cart
