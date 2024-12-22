import time
import pyautogui
from .base import SearchService
from ..core.browsers import EdgeBrowser
from ..core.text_manipulation import TextManipulation
from ..config import AutomationConfig


class ChatGPTSearch(SearchService):
    """ChatGPT search implementation"""

    def __init__(self):
        self.browser = EdgeBrowser()

    def format_query(self, query: str) -> str:
        return f"{query} start by saying [STARTING] and end by saying [ENDING]"

    def process_response(self, response: str) -> str:
        ist = response.find("[STARTING]")
        est = response.find("[ENDING]")
        text_v1 = response[response.find("[STARTING]", ist + 1) + 10:response.find("[ENDING]",
                                                                                   est + 1)].strip()
        return text_v1

    def perform_search(self, query: str) -> str:
        formatted_query = self.format_query(query)
        try:
            self.browser.search_and_enter(formatted_query)
            start_time = time.time()
            while True:
                time.sleep(AutomationConfig.delays.chatgpt_text_process_time)
                text = TextManipulation.get_clipboard_content()

                if text.count("[ENDING]") > 1 or \
                    (time.time() - start_time > AutomationConfig.delays.max_search_time):
                    return self.process_response(text)


        except Exception as e:
            print(f"Error performing search: {e}")
            return ""
