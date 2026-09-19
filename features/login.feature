@smoke
Feature: User login

	Background:
		Given the login page is open

	Scenario Outline: Successful login with valid credentials
		When the user logs in as "<user>" with password "<pwd>"
		Then the inventory page is displayed

		Examples:
			| user                      | pwd             |
			| standard_user             | secret_sauce    |
			| performance_glitch_user   | secret_sauce    |

	Scenario Outline: Error scenarios
		When the user logs in as "<user>" with password "<pwd>"
		Then an error "<message>" is shown

		Examples:
			| user            | pwd             | message               |
			| empty           | secret_sauce    | Username is required  |
			| problem_user    | secret_ketchup  | Username and password do not match any user in this service  |
			| locked_out_user | secret_sauce    | Sorry, this user has been locked out.  |