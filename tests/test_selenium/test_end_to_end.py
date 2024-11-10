""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n""" nModule Purpose: Briefly describe what this module does. nDependencies: List any dependencies required.n """n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""n"""nModule Purpose: Briefly describe what this module does.nDependencies: List any specific dependencies required.n"""nimport pytest
import time
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app
from threading import Thread
from config import TestConfig
import requests

# Helper functions
def find_free_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def run_server(app, port):
    app.run(port=port, use_reloader=False)

def wait_for_server(url, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get(url)
            return True
        except requests.ConnectionError:
            time.sleep(0.5)
    return False

# Fixtures
@pytest.fixture(scope="module")
def test_server():
    """Fixture to start and stop a Flask test server."""
    port = find_free_port()
    app = create_app(TestConfig)
    thread = Thread(target=run_server, args=(app, port))
    thread.daemon = True
    thread.start()
    
    server_url = f"http://127.0.0.1:{port}"
    if not wait_for_server(server_url):
        pytest.fail("Server did not start within the expected time.")
    
    yield server_url
    thread.join(timeout=5)  # Ensure thread stops within timeout

@pytest.fixture(scope="module")
def driver():
    """Fixture to initialize and quit the Selenium WebDriver."""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Test Cases
def test_register(driver, test_server):
    """End-to-end test for user registration."""
    driver.get(f"{test_server}/register")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").send_keys("seleniumuser")
    driver.find_element(By.NAME, "email").send_keys("seleniumuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.NAME, "confirm_password").send_keys("Password123")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Your account has been created!")
    )
    assert "Your account has been created!" in driver.page_source

def test_login(driver, test_server):
    """End-to-end test for user login."""
    driver.get(f"{test_server}/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

    driver.find_element(By.NAME, "email").send_keys("seleniumuser@example.com")
    driver.find_element(By.NAME, "password").send_keys("Password123")
    driver.find_element(By.TAG_NAME, "button").click()

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Login successful!")
    )
    assert "Login successful!" in driver.page_source
