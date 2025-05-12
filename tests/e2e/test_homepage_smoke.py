import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path


def get_sample_file_path(filename):
    project_root = Path(__file__).parent.parent.parent
    sample_file_path = project_root / "tests" / "sample_files" / filename
    if not sample_file_path.exists():
        raise FileNotFoundError(f"Sample file not found: {sample_file_path}")
    return str(sample_file_path.absolute())


@pytest.fixture
def chrome_driver():
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    yield driver
    driver.quit()


def test_upload_dictionary(run_app, chrome_driver):
    """
    E2E test for dictionary upload page.
    """

    wait = WebDriverWait(chrome_driver, 40)

    # ✅ Step 1: Go to Dictionary page
    chrome_driver.get(f"{run_app}/Dictionary")

    # ✅ Step 2: Confirm page title appears (not tab title)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    body_text = chrome_driver.find_element(By.TAG_NAME, "body").text
    assert "Manage Coding Dictionary" in body_text, f"Unexpected page content: {body_text}"


    # ✅ Step 3: Locate the file input
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )

    # ✅ Step 4: Upload the dictionary.csv file
    sample_file = get_sample_file_path("dictionary.csv")
    file_input.send_keys(sample_file)

    # ✅ Step 5: Wait for success message
    success_msg = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Dictionary uploaded')]")
        )
    )

    assert "uploaded" in success_msg.text.lower()
