# tests/e2e/test_dictionary.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_dictionary_page_loads(run_app, driver):
    url = f"{run_app.rstrip('/')}/Dictionary"
    driver.get(url)
    header = driver.find_element(By.TAG_NAME, "h1")
    assert "Manage Coding Dictionary" in header.text
