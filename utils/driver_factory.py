from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Shared with CheckoutPage, which needs to know where to look for the
# downloaded receipt. Anchored to the repo root, not cwd-relative.
DOWNLOAD_DIR = Path(__file__).resolve().parent.parent / "downloads"


class DriverFactory:

    @staticmethod
    def get_driver(browser="chrome", headless=False):
        if browser == "chrome":
            DOWNLOAD_DIR.mkdir(exist_ok=True)
            options = Options()
            if headless:
                # CI runners have no display. --start-maximized has no effect
                # headless, so pin an explicit window size instead - some
                # sites lay out elements differently (or not at all) below a
                # certain viewport width.
                options.add_argument("--headless=new")
                options.add_argument("--window-size=1920,1080")
            else:
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
                    "download.default_directory": str(DOWNLOAD_DIR),
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                },
            )
            return webdriver.Chrome(options=options)
        elif browser == "firefox":
            from selenium.webdriver.firefox.options import Options as FirefoxOptions

            firefox_options = FirefoxOptions()
            if headless:
                firefox_options.add_argument("--headless")
                firefox_options.add_argument("--width=1920")
                firefox_options.add_argument("--height=1080")
            return webdriver.Firefox(options=firefox_options)
        elif browser == "edge":
            return webdriver.Edge()
        raise ValueError(f"Unsupported browser: {browser}")
