# Created by denis_petelin at 10/11/18
Feature: When I toggle Task complete it changes color
  This example is bad, but thats what I was crafted late in the night...

  Scenario: Main Success
    Given I'm registered user
    And I have task pending
    When I log in I see my tasks and toggle button is blue
    When I click "complete"
    Then task toggle turns red