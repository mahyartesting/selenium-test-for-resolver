import pytest
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

config = configparser.ConfigParser()
config.read("config.ini")


@pytest.fixture(scope="session")
def browser():
    """
    Sets up a session-scoped WebDriver based on the browser specified in the config.ini file
    """
    browser_name = config["DEFAULT"]["browser"].lower()
    driver = None
    if browser_name == "edge":
        driver_path = config["DRIVER_PATHS"]["edge"]
        service = EdgeService(driver_path)
        driver = webdriver.Edge(service=service)
    elif browser_name == "chrome":
        driver_path = config["DRIVER_PATHS"]["chrome"]
        service = ChromeService(driver_path)
        driver = webdriver.Chrome(service=service)
    elif browser_name == "firefox":
        driver_path = config["DRIVER_PATHS"]["firefox"]
        service = FirefoxService(driver_path)
        driver = webdriver.Firefox(service=service)
    yield driver
    driver.quit()


@pytest.fixture
def go_to_home_page(browser):
    home_url = config["DEFAULT"]["home_url"]
    browser.get(home_url)
    return browser


@pytest.fixture
def get_table_cell_value():
    def _get_cell_value(table, row, col):
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        cells = rows[row].find_elements(By.TAG_NAME, "td")
        return cells[col].text

    return _get_cell_value
