Feature: Login Functionality
  As a user, I want to login to Swag Labs to access the products.

  @smoke
  Scenario: Successful Login
    Given the user is on the login page
    When the user enters valid credentials
    Then the user should be redirected to the inventory page

  @regression
  Scenario Outline: Failed Login Attempts
    Given the user is on the login page
    When the user enters "<username>" and "<password>"
    Then an error message "<error_message>" is displayed
    Examples:
      | username        | password     | error_message                                                             |
      | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                       |
      | standard_use    | secret_sauce | Epic sadface: Username and password do not match any user in this service |
      | standard_user   | secret_sauc  | Epic sadface: Username and password do not match any user in this service |