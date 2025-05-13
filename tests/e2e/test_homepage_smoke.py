import pytest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)


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
    
    # Add a longer delay before navigating to ensure the server is fully ready
    time.sleep(5)
    
    # ✅ Step 1: First navigate to the base URL to ensure the app is loaded properly
    base_url = run_app.rstrip('/')
    logging.info(f"Navigating to base URL: {base_url}")
    chrome_driver.get(base_url)
    
    # Wait for initial page load
    time.sleep(3)
    chrome_driver.save_screenshot("base_page_debug.png")
    
    # Then navigate to the Dictionary page
    logging.info(f"Navigating to Dictionary page: {base_url}/Dictionary")
    chrome_driver.get(f"{base_url}/Dictionary")
    
    # Take a screenshot for debugging (useful in CI environments)
    chrome_driver.save_screenshot("dictionary_page_debug_1.png")
    
    # Print out the page source for debugging
    logging.info(f"Page source: {chrome_driver.page_source[:500]}...")  # First 500 chars
    
    try:
        # Try multiple approaches to find the content
        logging.info("Waiting for page to stabilize...")
        time.sleep(10)  # Allow more time for Streamlit to fully render
        chrome_driver.save_screenshot("dictionary_page_debug_2.png")
        
        # Retry strategy for getting page content
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logging.info(f"Attempt {attempt+1} to get page content")
                
                # Check if we need to refresh the page
                if attempt > 0:
                    logging.info("Refreshing page")
                    chrome_driver.refresh()
                    time.sleep(5)
                
                # Try different selectors to find content
                selectors_to_try = [
                    (By.TAG_NAME, "body"),
                    (By.TAG_NAME, "main"),
                    (By.CLASS_NAME, "stApp"),
                    (By.XPATH, "//div[contains(@class, 'main')]"),
                    (By.XPATH, "//h1[contains(text(), 'Manage Coding Dictionary')]"),
                ]
                
                for selector_type, selector in selectors_to_try:
                    try:
                        logging.info(f"Trying selector: {selector_type}={selector}")
                        element = wait.until(EC.presence_of_element_located((selector_type, selector)))
                        body_text = element.text
                        logging.info(f"Found text with selector {selector_type}={selector}: {body_text[:100]}...")
                        
                        # If we found our expected content, proceed with the test
                        if "Manage Coding Dictionary" in body_text:
                            logging.info("Found 'Manage Coding Dictionary' in the page!")
                            
                            # ✅ Step 3: Locate the file input
                            logging.info("Looking for file input...")
                            file_input = wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                            )
                        
                            # ✅ Step 4: Upload the dictionary.csv file
                            sample_file = get_sample_file_path("dictionary.csv")
                            logging.info(f"Uploading file: {sample_file}")
                            file_input.send_keys(sample_file)
                        
                            # ✅ Step 5: Wait for success message
                            logging.info("Waiting for success message...")
                            success_msg = wait.until(
                                EC.presence_of_element_located(
                                    (By.XPATH, "//*[contains(text(),'Dictionary uploaded')]")
                                )
                            )
                        
                            assert "uploaded" in success_msg.text.lower()
                            logging.info("Test completed successfully!")
                            return  # Exit the function successfully
                    except (TimeoutException, StaleElementReferenceException) as e:
                        logging.info(f"Selector {selector_type}={selector} failed: {str(e)}")
                        continue
                
                # If we're here, we couldn't find the content with any selector
                logging.warning(f"Attempt {attempt+1}: Could not find 'Manage Coding Dictionary' with any selector")
            
            except Exception as e:
                logging.error(f"Error in attempt {attempt+1}: {str(e)}")
                chrome_driver.save_screenshot(f"error_attempt_{attempt+1}.png")
        
        # If we've exhausted all retries and approaches, check what's actually on the page
        logging.error("All attempts failed. Checking final page state...")
        chrome_driver.save_screenshot("final_state.png")
        body_text = chrome_driver.find_element(By.TAG_NAME, "body").text
        
        # Try to get the Streamlit app content specifically
        try:
            app_content = chrome_driver.find_element(By.CLASS_NAME, "stApp").text
            logging.error(f"Streamlit app content: {app_content}")
        except Exception:
            logging.error("Could not find Streamlit app content")
        
        # Final assertion to fail the test with useful info
        assert "Manage Coding Dictionary" in body_text, f"Content not found after multiple attempts. Final page content: {body_text}"
    
    except Exception as e:
        # Capture as much information as possible
        logging.error(f"Test failed with exception: {str(e)}")
        chrome_driver.save_screenshot("test_failure_final.png")
        
        # Try to get URLs
        logging.error(f"Current URL: {chrome_driver.current_url}")
        logging.error(f"Page title: {chrome_driver.title}")
        
        # Re-raise the exception to fail the test
        raise