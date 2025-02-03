from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAgent(ABC):
    """Abstract base class for chatbot agents."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def handle_request(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a user request and return a structured response."""
        pass