from abc import ABC, abstractmethod
import os
import time
import pyautogui
from ..config import AutomationConfig


class BrowserAutomation(ABC):
    """Abstract base class for browser automation"""

    @abstractmethod
    def open_browser(self) -> bool:
        """Open the browser"""
        pass

    @classmethod
    def close_browser(cls) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'w')
            return True
        except Exception as e:
            print(f"Error closing browser: {e}")
            return False


    @classmethod
    def search_and_enter(cls,search_text):
        """Type and search for given text"""
        try:
            pyautogui.write(search_text)
            pyautogui.press('enter')
            time.sleep(AutomationConfig.delays.search_delay)
            return True
        except Exception as e:
            print(f"Error performing search: {e}")
            return False

class EdgeBrowser(BrowserAutomation):
    """Microsoft Edge browser implementation"""

    @classmethod
    def open_browser(cls) -> bool:
        try:
            os.system("microsoft-edge-stable")
            time.sleep(AutomationConfig.delays.edge_open_delay)
            return True
        except Exception as e:
            print(f"Error opening Edge: {e}")
            return False



class ChromeBrowser(BrowserAutomation):
    """Google Chrome browser implementation"""

    @classmethod
    def open_browser(cls) -> bool:
        try:
            os.system("google-chrome")
            time.sleep(AutomationConfig.delays.chrome_open_delay)
            return True
        except Exception as e:
            print(f"Error opening Chrome: {e}")
            return False



class FirefoxBrowser(BrowserAutomation):
    """Mozilla Firefox browser implementation"""

    @classmethod
    def open_browser(cls) -> bool:
        try:
            os.system("firefox")
            time.sleep(AutomationConfig.delays.firefox_open_delay)
            return True
        except Exception as e:
            print(f"Error opening Firefox: {e}")
            return False

