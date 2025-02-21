"""Factory for creating LLM clients"""
from typing import Optional
from .llm_base import BaseLLMClient, LLMProvider
from .llm_gemini import GeminiClient

class LLMFactory:
    """Factory for creating LLM clients"""
    
    @staticmethod
    def create(provider: LLMProvider, api_key: Optional[str] = None) -> BaseLLMClient:
        """Create an LLM client"""
        if provider == LLMProvider.GEMINI:
            return GeminiClient(api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
