import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

# Set up logging - make sure it prints to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create dedicated test logger function for visibility
def test_log(message):
    logger.info(message)
    print(f"TEST LOG: {message}")

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
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(90)  # Extended timeout
    yield driver
    driver.quit()

def test_upload_dictionary(run_app, chrome_driver):
    """
    Simplified E2E test for dictionary upload page - just verifies page load.
    """
    # Simplify test to focus on core functionality
    test_log("Starting test_upload_dictionary test")
    
    # Create a wait object
    wait = WebDriverWait(chrome_driver, 90)
    
    # Step 1: First navigate to the base URL
    base_url = run_app.rstrip('/')
    test_log(f"Navigating to base URL: {base_url}")
    chrome_driver.get(base_url)
    
    # Wait for initial page load
    test_log("Waiting for initial page to load...")
    time.sleep(5)
    chrome_driver.save_screenshot("base_page.png")
    
    # Step 2: Navigate to Dictionary page
    dictionary_url = f"{base_url}/Dictionary"
    test_log(f"Navigating to Dictionary page: {dictionary_url}")
    chrome_driver.get(dictionary_url)
    
    # Wait for page load
    test_log("Waiting for Dictionary page to load...")
    time.sleep(10)
    chrome_driver.save_screenshot("dictionary_page.png")
    
    # Try to find content using different approaches
    test_log("Attempting to find page content...")
    
    # Try explicit wait for page title/content
    try:
        test_log("Waiting for page title to appear...")
        title = wait.until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='📚 Manage Coding Dictionary']"))
        )
        test_log(f"Found title: {title.text}")
        
        # If we get here, the test passed - the page loaded correctly
        test_log("Page loaded successfully with correct title!")
        
        # Only proceed with file upload if title was found
        test_log("Looking for file upload input...")
        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Upload the dictionary file
        sample_file = get_sample_file_path("dictionary.csv")
        test_log(f"Uploading file: {sample_file}")
        file_input.send_keys(sample_file)
        
        # Wait for success message
        test_log("Waiting for upload success message...")
        success_msg = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Dictionary uploaded')]")
            )
        )
        
        test_log(f"Found success message: {success_msg.text}")
        assert "uploaded" in success_msg.text.lower()
        test_log("Test completed successfully!")
        
    except Exception as e:
        # Log exception details
        test_log(f"Exception occurred: {str(e)}")
        
        # Try to get body content as fallback
        try:
            test_log("Trying to get body content...")
            body = chrome_driver.find_element(By.TAG_NAME, "body")
            test_log(f"Body text: {body.text[:500]}")
        except Exception as body_e:
            test_log(f"Could not get body text: {str(body_e)}")
        
        # Try to get page source
        try:
            test_log("Getting page source...")
            page_source = chrome_driver.page_source
            test_log(f"Page source (first 500 chars): {page_source[:500]}")
        except Exception as source_e:
            test_log(f"Could not get page source: {str(source_e)}")
        
        # Take final screenshot
        chrome_driver.save_screenshot("test_failure.png")
        
        # If we got this far without finding content, fail the test
        raise