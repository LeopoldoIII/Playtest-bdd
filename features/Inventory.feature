Feature: Inventory Functionality
  As a user, I want to interact with the inventory page.

  Scenario: Select item
    Given the user is on the login page
    When the user enters "standard_user" and "secret_sauce"
    Then the user should be redirected to the inventory page
    When the user adds "Sauce Labs Backpack" to the cart
    Then the "Sauce Labs Backpack" button changes to "Remove"
    Then the shop icon changes to "1"
    When the user adds "Sauce Labs Onesie" to the cart
    Then the "Sauce Labs Onesie" button changes to "Remove"
    Then the shop icon changes to "2"

