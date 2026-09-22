from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverFactory:

    @staticmethod
    def get_driver(browser="chrome"):
        if browser == "chrome":
            options = Options()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            # Test creds like "secret_sauce" match Chrome's public breach
            # list, so it pops a native "Change your password" dialog mid-
            # test that silently eats clicks on whatever's underneath it.
            # Disable the password manager / leak-detection UI entirely.
            options.add_argument("--disable-features=PasswordLeakDetection,PasswordManagerRedesign")
            options.add_experimental_option(
                "prefs",
                {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False,
                    "profile.password_manager_leak_detection": False,
                },
            )
            return webdriver.Chrome(options=options)
        elif browser == "firefox":
            return webdriver.Firefox()
        elif browser == "edge":
            return webdriver.Edge()
        raise ValueError(f"Unsupported browser: {browser}")
