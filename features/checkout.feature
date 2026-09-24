@smoke @checkout
Feature: Checkout page

	Scenario: A logged-in user can add products, check out, and download the receipt
		Given the login page is open
		When the user logs in as "standard_user" with password "secret_sauce"
		Then the inventory page is displayed
		And the user should be able to add products to cart
		Then the user should be able to navigate to cart page
		Then the user navigates to checkout page
		And the user enters information on checkout and clicks continue
		Then the subtotal price should match with the prices displayed in inventory page
		And the user submits the order
		Then the user downloads the receipt
