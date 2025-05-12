@pytest.fixture(scope="session")
def run_app():
    import socket
    import subprocess
    import time
    import requests

    process = subprocess.Popen(
        ["streamlit", "run", "app/Home.py", "--server.port", "8501"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    base_url = "http://localhost:8501/"
    max_retries = 60
    wait_seconds = 1

    for _ in range(max_retries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if sock.connect_ex(("localhost", 8501)) == 0:
                    response = requests.get(base_url)
                    dict_response = requests.get(base_url + "Dictionary")
                    if response.status_code == 200 and dict_response.status_code == 200:
                        break
        except (socket.error, requests.RequestException):
            pass
        time.sleep(wait_seconds)
    else:
        if process.stdout:
            print("=== Streamlit STDOUT ===")
            print(process.stdout.read())

        if process.stderr:
            print("=== Streamlit STDERR ===")
            print(process.stderr.read())

        process.terminate()
        process.wait(timeout=5)
        raise RuntimeError("Failed to start Streamlit application")

    try:
        yield base_url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
