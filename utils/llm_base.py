"""Base classes for LLM clients"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union
from enum import Enum

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    
class BaseLLMClient(ABC):
    """Base class for LLM clients"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    @abstractmethod
    async def analyze_image(
        self,
        image_url: str,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Analyze an image using the LLM"""
        pass
        
    @abstractmethod
    async def analyze_image_stream(
        self,
        image_url: str,
        prompt: str,
        expect_json: bool = False
    ):
        """Stream image analysis results from the LLM"""
        pass
        
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Generate text using the LLM"""
        pass
