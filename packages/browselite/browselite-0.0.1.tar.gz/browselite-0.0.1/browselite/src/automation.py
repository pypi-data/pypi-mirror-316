from typing import Dict, Optional, Literal
import pyautogui
from browselite.src.services.chatgpt import ChatGPTSearch
from browselite.src.services.base import SearchService

SearchServiceType = Literal["openai","google"]

_SERVICE_NAME_MAP = {
    "chatgptsearch":"chatgpt",
    "chatgpt":"chatgpt",
    "openai":"chatgpt"
}

class AutomationManager:
    """Main automation manager class"""

    def __init__(self):
        pyautogui.FAILSAFE = True
        self.search_services: Dict= {
            "chatgpt": ChatGPTSearch()
        }

    def execute_search(self, query: str, service_name: SearchServiceType="google") -> Optional[str]:
        """Execute a search using the specified service"""
        name = _SERVICE_NAME_MAP.get(service_name, "google")
        query = f"https://www.{name}.com/search?q={query}"

        service:ChatGPTSearch = self.search_services.get(name)

        if not service:
            print(f"Service {service_name} not found")
            return None

        if not service.browser.open_browser():
            return None

        try:
            result = service.perform_search(query)
            return result
        finally:
            service.browser.close_browser()