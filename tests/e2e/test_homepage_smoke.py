# tests/e2e/test_dictionary_page_loads.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def test_dictionary_page_loads(run_app, driver):
    # Streamlit multipage apps use ?page=<Name> to select pages
    url = run_app.rstrip("/") + "/?page=Dictionary"
    driver.get(url)

    # find any element that contains our page title text
    elem = driver.find_element(
        By.XPATH,
        "//*[contains(text(), 'Manage Coding Dictionary')]"
    )
    assert elem is not None
