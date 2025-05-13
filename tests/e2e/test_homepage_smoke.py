import pytest
import time
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
    # Add user agent to appear more like a normal browser
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    # Disable web security to avoid CORS issues
    options.add_argument("--disable-web-security")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    yield driver
    driver.quit()


def test_upload_dictionary(run_app, chrome_driver):
    """
    E2E test for dictionary upload page.
    """
    # Create a wait object with a longer timeout for CI environments
    wait = WebDriverWait(chrome_driver, 60)
    
    # Add a small delay before navigating to ensure the server is fully ready
    time.sleep(2)
    
    # ✅ Step 1: Go to Dictionary page - ensure trailing slash is consistent
    base_url = run_app.rstrip('/')
    chrome_driver.get(f"{base_url}/Dictionary")
    
    # Take a screenshot for debugging (useful in CI environments)
    chrome_driver.save_screenshot("dictionary_page_debug.png")
    
    # Print out the page source for debugging
    print(f"Page source: {chrome_driver.page_source[:500]}...")  # First 500 chars
    
    try:
        # ✅ Step 2: Confirm page title appears (not tab title)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = chrome_driver.find_element(By.TAG_NAME, "body").text
        
        # Check for 403 error specifically and provide better error message
        if "403: Forbidden" in body_text:
            print("403 Forbidden detected - attempting to navigate to base URL first")
            # Try navigating to the base URL first, then to the Dictionary page
            chrome_driver.get(base_url)
            time.sleep(3)  # Give it time to load
            chrome_driver.get(f"{base_url}/Dictionary")
            time.sleep(2)
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
    
    except Exception as e:
        # Take a screenshot on failure for debugging
        chrome_driver.save_screenshot("dictionary_test_failure.png")
        # Re-raise the exception to fail the test
        raise e