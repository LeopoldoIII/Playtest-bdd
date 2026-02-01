Feature: Inventory Data Extraction
  As a user I want to scrape product information from the inventory page
  So that I can analyze prices and descriptions externally

  Scenario: Scrape all inventory items to a JSON file
    Given the user is on the login page
    When the user enters "standard_user" and "secret_sauce"
    Then the user should be redirected to the inventory page
    And the user exports all product data to "inventory_data.json"