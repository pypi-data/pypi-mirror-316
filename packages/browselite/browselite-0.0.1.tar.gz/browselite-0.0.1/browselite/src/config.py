from dataclasses import dataclass, field
from typing import Dict, Any

from pydantic import BaseModel, Field


@dataclass
class Delays:
    safety_delay: int = 2
    edge_open_delay: int = 3
    chrome_open_delay:int = 3
    firefox_open_delay:int=3
    search_delay: int = 5
    max_search_time: int = 20
    chatgpt_text_process_time = 1


@dataclass
class AutomationConfig:
    """Configuration class for automation settings"""
    delays: Any = Delays
