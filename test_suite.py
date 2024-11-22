import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


# Test 1: Verify the presence of email, password fields, and sign-in button, and test their functionality.
@pytest.mark.parametrize(
    "div_id,email,password",
    [("test-1-div", config["USER"]["email"], config["USER"]["password"])],
)
def test_email_password_fields(go_to_home_page, div_id, email, password):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    email_field = test_div.find_element(By.ID, "inputEmail")
    assert email_field is not None, "Email field not found"
    password_field = test_div.find_element(By.ID, "inputPassword")
    assert password_field is not None, "Password field not found!"
    sign_in_button = test_div.find_element(By.CLASS_NAME, "btn-primary")
    assert sign_in_button is not None, "Sign-in button not found!"
    email_field.send_keys(email)
    password_field.send_keys(password)


# Test 2: Verify the list group items and their properties.
@pytest.mark.parametrize("div_id", ["test-2-div"])
def test_list_group_items(go_to_home_page, div_id):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    list_items = test_div.find_elements(By.CLASS_NAME, "list-group-item")
    assert len(list_items) == 3, "List group does not contain exactly 3 items!"
    second_item = list_items[1]
    assert "List Item 2" in second_item.text, "Second list item text is incorrect!"
    badge = second_item.find_element(By.CLASS_NAME, "badge")
    assert badge.text == "6", "Second list item badge value is incorrect!"


# Test 3: Verify the default value and functionality of the dropdown menu.
@pytest.mark.parametrize("div_id", ["test-3-div"])
def test_dropdown(go_to_home_page, div_id):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    dropdown_button = test_div.find_element(By.ID, "dropdownMenuButton")
    assert (
        dropdown_button.text == "Option 1"
    ), "Default dropdown value is not 'Option 1'!"
    dropdown_button.click()
    option_3 = test_div.find_element(
        By.XPATH, "//a[@class='dropdown-item' and text()='Option 3']"
    )
    option_3.click()
    assert (
        dropdown_button.text == "Option 3"
    ), "Dropdown value did not change to 'Option 3'!"


# Test 4: Verify the states of the buttons in the test div.
@pytest.mark.parametrize("div_id", ["test-4-div"])
def test_buttons(go_to_home_page, div_id):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    first_button = test_div.find_element(By.CLASS_NAME, "btn-primary")
    second_button = test_div.find_element(By.CLASS_NAME, "btn-secondary")
    assert first_button.is_enabled(), "First button is not enabled!"
    assert not second_button.is_enabled(), "Second button is not disabled!"


# Test 5: Verify the dynamic button's appearance, click action, and resulting success message.
@pytest.mark.parametrize("div_id", ["test-5-div"])
def test_dynamic_button(go_to_home_page, div_id):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    button = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "test5-button"))
    )
    button.click()
    alert = test_div.find_element(By.ID, "test5-alert")
    assert alert.is_displayed(), "Success message is not displayed!"
    assert "You clicked a button!" in alert.text, "Success message text is incorrect!"
    assert not button.is_enabled(), "Button is not disabled after clicking!"


# Test 6: Verify the value of a specific cell in the table.
@pytest.mark.parametrize("div_id", ["test-6-div"])
def test_table_cell_value(go_to_home_page, div_id, get_table_cell_value):
    browser = go_to_home_page
    test_div = browser.find_element(By.ID, div_id)
    table = test_div.find_element(By.CLASS_NAME, "table")
    cell_value = get_table_cell_value(table, 2, 2)
    assert cell_value == "Ventosanzap", "Cell value at (2, 2) is incorrect!"
