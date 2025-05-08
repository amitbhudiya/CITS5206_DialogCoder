"""
E2E test for homepage and file upload functionality using Selenium.
"""

from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_sample_file_path(filename):
    """
    Get the absolute path to a sample file in the tests/sample_files directory.

    Args:
        filename (str): Name of the sample file

    Returns:
        str: Absolute path to the sample file
    """
    # Get the absolute path to the project root
    project_root = Path(__file__).parent.parent.parent

    # Construct the path to the sample file
    sample_file_path = project_root / "tests" / "sample_files" / filename

    if not sample_file_path.exists():
        raise FileNotFoundError(f"Sample file not found: {sample_file_path}")

    return str(sample_file_path.absolute())


@pytest.fixture
def chrome_driver():
    """
    Set up and tear down a headless Chrome WebDriver.

    Yields:
        webdriver.Chrome: The Chrome WebDriver instance
    """
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)

    try:
        yield driver
    finally:
        # Ensure driver quits even if test fails
        driver.quit()


def test_upload_dictionary(run_app, chrome_driver):
    """
    Smoke test for the homepage and dictionary upload functionality.

    Test steps:
    1. Open the app root URL
    2. Check if the page title contains "Transcript Coder" (or the expected title)
    3. Locate the file upload widget and Upload button
    4. Upload a sample dictionary CSV file
    5. Click the Upload button
    6. Wait for a success message to appear

    Args:
        run_app (str): URL of the running Streamlit app (from fixture)
        chrome_driver (webdriver.Chrome): Chrome WebDriver instance (from fixture)
    """
    # Explicitly define wait time for all async operations
    wait_time = 30  # seconds
    wait = WebDriverWait(chrome_driver, wait_time)

    # Step 1: Navigate to the app
    chrome_driver.get(run_app)

    # Step 2: Verify the page title
    expected_title = "Transcript Coder"
    try:
        # Allow for slightly different title formats
        wait.until(lambda d: expected_title.lower() in d.title.lower())
    except Exception as e:
        actual_title = chrome_driver.title
        raise AssertionError(
            f"Page title verification failed. Expected title to contain '{expected_title}', "
            f"but got '{actual_title}'. Error: {str(e)}"
        )

    # Step 3: Locate the file upload widget
    try:
        # Streamlit file uploader has specific structure - we need to find the file input
        # Note: May need adjusting based on the actual app structure
        file_uploader = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
    except Exception as e:
        raise AssertionError(f"Could not find file upload widget. Error: {str(e)}")

    # Step 4: Prepare and upload the dictionary file
    sample_file = get_sample_file_path("dictionary.csv")

    try:
        # Send the file path to the file input
        file_uploader.send_keys(sample_file)
    except Exception as e:
        raise AssertionError(f"Failed to upload the file. Error: {str(e)}")

    # Step 5: Find and click the Upload button
    try:
        # Look for the upload button - adjust selector based on your app's structure
        upload_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(text(), 'Upload') or contains(@aria-label, 'Upload')]",
                )
            )
        )
        # Click the upload button
        upload_button.click()
    except Exception as e:
        raise AssertionError(
            f"Could not find or click the Upload button. Error: {str(e)}"
        )

    # Step 6: Wait for success message
    try:
        # Look for success message - adjust selector based on actual app
        success_message = wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(), 'Dictionary uploaded') or contains(text(), 'Upload successful')]",
                )
            )
        )
        # Verify message is displayed
        assert success_message.is_displayed(), "Success message is not visible"
    except Exception as e:
        raise AssertionError(f"Upload success message did not appear. Error: {str(e)}")
