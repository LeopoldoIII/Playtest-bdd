Feature: Login Functionality
  As a user, I want to login to Swag Labs to access the products.

  Scenario: Successful Login
    Given the user is on the login page
    When the user enters "standard_user" and "secret_sauce"
    Then the user should be redirected to the inventory page

  Scenario: Failed Login
    Given the user is on the login page
    When the user enters "locked_out_user" and "secret_sauce"
    Then an error message "Epic sadface: Sorry, this user has been locked out." is displayed