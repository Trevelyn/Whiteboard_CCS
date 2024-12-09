import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def setup_driver():
    """Initialize the Edge browser in private mode."""
    options = webdriver.EdgeOptions()
    options.add_argument("-inprivate")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.set_window_size(945, 1012)
    return driver

def authenticate_user(driver, username, password):
    """Sign in a user to the application."""
    try:
        driver.get("https://whiteboard.office.com/")
        
        # Enter username
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "i0116"))).send_keys(username)
        driver.find_element(By.ID, "idSIButton9").click()

        # Wait for password input and enter password
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(password)
        driver.find_element(By.ID, "idSIButton9").click()
        
        # Wait for additional authentication if needed
        WebDriverWait(driver, 20).until(EC.url_contains("whiteboard.office.com"))
    except Exception as e:
        raise RuntimeError(f"Authentication failed for user {username}: {e}")

def click_board_picker_settings(driver):
    """Click the boardPickerSettingsButton."""
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".boardPickerSettingsButton"))
        )
        button.click()
        time.sleep(2)  # Allow the menu to render
    except Exception as e:
        raise RuntimeError(f"Failed to click boardPickerSettingsButton: {e}")

def check_button_existence(driver, css_selector):
    """Verify if a button exists by its CSS selector."""
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return True
    except:
        return False

def sign_out_user(driver):
    """Sign out the current user with enhanced debugging."""
    try:
        # Ensure profile picture is interactable
        profile_picture = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".\\_8ZYZKvxC8bvw1xgQGSkvvA\\=\\= > img"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_picture)
        profile_picture.click()
        time.sleep(2)  # Allow menu to open
        
        # Click on sign-out button
        sign_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "mectrl_body_signOut"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", sign_out_button)
        sign_out_button.click()
        time.sleep(5)  # Wait for the sign-out process to complete
    except Exception as e:
        raise RuntimeError(f"Sign-out failed: {e}")

def test_privacy_and_security_button():
    """Test visibility of the privacy and security button for two users."""
    driver = setup_driver()
    try:
        # Test for User A
        print("Testing for User A...")
        authenticate_user(driver, "AdeleV@M365x41049209.OnMicrosoft.com", "Kenya@2023")
        click_board_picker_settings(driver)
        privacy_button_exists = check_button_existence(driver, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
        assert privacy_button_exists, "Privacy and Security button should be visible for User A."
        print("Test Passed: Privacy and Security button exists for User A.")
        sign_out_user(driver)

        # Test for User B
        print("Testing for User B...")
        authenticate_user(driver, "AlexW@M365x41049209.OnMicrosoft.com", "Kenya@2023")
        click_board_picker_settings(driver)
        privacy_button_exists = check_button_existence(driver, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
        assert not privacy_button_exists, "Privacy and Security button should NOT be visible for User B."
        print("Test Passed: Privacy and Security button does not exist for User B.")

    except AssertionError as ae:
        print(f"Test Failed: {ae}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_privacy_and_security_button()
