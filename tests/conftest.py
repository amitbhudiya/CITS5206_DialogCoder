"""
Pytest configuration and fixtures for DialogCoder application tests.
"""

import socket
import subprocess
import time

import pytest
import requests


@pytest.fixture(scope="session")
def run_app():
    """
    Launch the Streamlit app as a background process for testing.

    This fixture:
    1. Starts the Streamlit app on port 8501
    2. Waits for the port to be responsive
    3. Yields the base URL to the test
    4. Terminates the process after tests are complete
    """
    # Start Streamlit in a background process
    process = subprocess.Popen(
        ["streamlit", "run", "app/Home.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    base_url = "http://localhost:8501/"

    # Wait for the server to start
    max_retries = 60
    wait_seconds = 1

    for _ in range(max_retries):
        try:
            # Check if port is open
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex(("localhost", 8501)) == 0:
                    # Verify app is responding
                    response = requests.get(base_url)
                    if response.status_code == 200:
                        break
        except (socket.error, requests.RequestException):
            pass

        time.sleep(wait_seconds)
    else:
        # If we get here, the server didn't start properly
        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError("Failed to start Streamlit application")

    # Yield the base URL to the test
    try:
        yield base_url
    finally:
        # Teardown: terminate the process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
