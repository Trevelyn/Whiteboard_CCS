import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)


def setup_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("-inprivate")
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.set_window_size(945, 1012)
    return driver


def authenticate_user(driver, username, password):
    try:
        driver.get("https://whiteboard.office.com/")

        # Enter username
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "i0116"))).send_keys(username)
        driver.find_element(By.ID, "idSIButton9").click()

        # Wait for password input and enter password
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "i0118"))).send_keys(password)
        driver.find_element(By.ID, "idSIButton9").click()

        # Wait for successful login
        WebDriverWait(driver, 20).until(EC.url_contains("whiteboard.office.com"))
    except Exception as e:
        raise RuntimeError(f"Authentication failed for user {username}: {e}")


def click_board_picker_settings(driver):
    try:
        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".boardPickerSettingsButton"))
        )
        button.click()
        time.sleep(2)  # Allow the menu to render
    except Exception as e:
        raise RuntimeError(f"Failed to click boardPickerSettingsButton: {e}")


def check_button_existence(driver, css_selector):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return True
    except:
        return False


def sign_out_and_restart(driver):
    try:
        # Step 1: Open user menu and sign out
        profile_picture = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".\\_8ZYZKvxC8bvw1xgQGSkvvA\\=\\= > img"))
        )
        profile_picture.click()
        time.sleep(2)  # Allow menu to open

        sign_out_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "mectrl_body_signOut"))
        )
        sign_out_button.click()
        time.sleep(3)  # Wait for sign-out

        # Restart the browser
        driver.quit()
        time.sleep(2)
        return setup_driver()
    except Exception as e:
        raise RuntimeError(f"Sign-out and restart failed: {e}")


class PrivacyAndSecurityButtonTest(unittest.TestCase):
    """Unit test for Privacy and Security button visibility."""
    
    # Class-level variable to store cumulative test results
    test_results = {"Total": 0, "Passed": 0, "Failed": 0}

    def setUp(self):
        """Setup the browser before each test case."""
        self.driver = setup_driver()

    def tearDown(self):
        """Close the browser after tests."""
        self.driver.quit()

    def test_user_a_privacy_button(self):
        """Test that Privacy and Security button is visible for User A."""
        print("Testing for User A...")
        try:
            PrivacyAndSecurityButtonTest.test_results["Total"] += 1
            authenticate_user(self.driver, "AdeleV@M365x41049209.OnMicrosoft.com", "Kenya@2023")
            click_board_picker_settings(self.driver)
            button_exists = check_button_existence(self.driver, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            self.assertTrue(button_exists, "Privacy and Security button should be visible for User A.")
            print(Fore.GREEN + "Test Passed: Privacy and Security button exists for User A.")
            PrivacyAndSecurityButtonTest.test_results["Passed"] += 1
        except Exception as e:
            print(Fore.RED + f"Test Failed: {e}")
            PrivacyAndSecurityButtonTest.test_results["Failed"] += 1
        finally:
            self.driver = sign_out_and_restart(self.driver)

    def test_user_b_privacy_button(self):
        """Test that Privacy and Security button is NOT visible for User B."""
        print("Testing for User B...")
        try:
            PrivacyAndSecurityButtonTest.test_results["Total"] += 1
            authenticate_user(self.driver, "AlexW@M365x41049209.OnMicrosoft.com", "Kenya@2023")
            click_board_picker_settings(self.driver)
            button_exists = check_button_existence(self.driver, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            self.assertFalse(button_exists, "Privacy and Security button should NOT be visible for User B.")
            print(Fore.GREEN + "Test Passed: Privacy and Security button does not exist for User B.")
            PrivacyAndSecurityButtonTest.test_results["Passed"] += 1
        except Exception as e:
            print(Fore.RED + f"Test Failed: {e}")
            PrivacyAndSecurityButtonTest.test_results["Failed"] += 1

    @classmethod
    def test_report(cls):
        """Print test case summary report."""
        total_tests = cls.test_results["Total"]
        passed_tests = cls.test_results["Passed"]
        failed_tests = cls.test_results["Failed"]
        not_run_tests = total_tests - (passed_tests + failed_tests)

        print("\nTest Case Summary Report:")
        print(f"{Fore.GREEN}Passed: {passed_tests}")
        print(f"{Fore.RED}Failed: {failed_tests}")
        print(f"{Fore.LIGHTBLACK_EX}Not Run: {not_run_tests}")
        print(f"Total Tests: {total_tests}")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(PrivacyAndSecurityButtonTest("test_user_a_privacy_button"))
    suite.addTest(PrivacyAndSecurityButtonTest("test_user_b_privacy_button"))
    suite.addTest(PrivacyAndSecurityButtonTest("test_report"))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
