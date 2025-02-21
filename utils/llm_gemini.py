"""Gemini LLM client"""
import os
import json
import logging
from typing import Dict, Any, Union, Optional
import google.generativeai as genai
import aiohttp
from .llm_base import BaseLLMClient
from .url_converter import URLConverter

logger = logging.getLogger(__name__)

class GeminiClient(BaseLLMClient):
    """Client for Google's Gemini API"""
    
    def _process_json_stream(self, chunks: list) -> Dict[str, Any]:
        """Process a stream of chunks into a JSON object with enhanced cleaning"""
        # Join all chunks into a single string
        text = ''.join(chunks)
        logger.debug(f"Raw text length: {len(text)}")
        
        # Remove markdown if present
        if '```' in text:
            parts = text.split('```')
            if len(parts) >= 3:
                text = parts[1]
                if text.startswith('json'):
                    text = text[4:]
                logger.debug("Removed markdown formatting")
        
        # Clean up whitespace and find JSON boundaries
        text = text.strip()
        start = text.find('{')
        end = text.rfind('}')
        
        if start >= 0 and end >= 0:
            text = text[start:end + 1]
            logger.debug(f"Found JSON object from index {start} to {end}")
            
            # First try direct parse
            try:
                data = json.loads(text)
                if not isinstance(data, dict):
                    raise ValueError("Response is not a JSON object")
                logger.debug("Successfully parsed JSON on first attempt")
                return data
            except json.JSONDecodeError as e:
                logger.warning(f"Initial JSON parse failed: {str(e)}")
                
                # Enhanced JSON cleaning
                # 1. Basic cleanup
                text = text.replace('\n', ' ')  # Remove newlines
                text = ' '.join(text.split())   # Normalize whitespace
                
                # 2. Fix common JSON structural issues
                text = text.replace(',}', '}')  # Fix trailing commas in objects
                text = text.replace(',]', ']')  # Fix trailing commas in arrays
                text = text.replace('}"', '}, "')  # Fix missing commas between objects
                text = text.replace(']"', '], "')  # Fix missing commas between arrays
                text = text.replace('}{', '}, {')  # Fix missing commas between objects
                text = text.replace('][', '], [')  # Fix missing commas between arrays
                
                # 3. Fix quote issues
                text = text.replace('\\"', '"')  # Fix escaped quotes
                text = text.replace('""', '"')    # Fix double quotes
                
                # 4. Balance brackets and braces
                open_curly = text.count('{')
                close_curly = text.count('}')
                open_square = text.count('[')
                close_square = text.count(']')
                
                # Add missing closing braces/brackets
                if open_curly > close_curly:
                    text += '}' * (open_curly - close_curly)
                if open_square > close_square:
                    text += ']' * (open_square - close_square)
                
                logger.debug("Attempting JSON parse with enhanced cleaning")
                try:
                    data = json.loads(text)
                    if not isinstance(data, dict):
                        raise ValueError("Response is not a JSON object")
                    logger.debug("Successfully parsed JSON after cleaning")
                    return data
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"Failed to parse JSON after cleaning: {str(e)}")
                    logger.debug(f"Failed text: {text[:500]}...")
                    raise ValueError("LLM response was not valid JSON") from e
        
        logger.error("Could not find JSON object markers in response")
        raise ValueError("Could not find JSON object in response")
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        
        # Use provided API key or get from environment
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided or found in environment")
            
        # Configure and initialize the model
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-001')
        
        # Initialize URL converter
        self.url_converter = URLConverter()
        
    async def _fetch_image(self, image_url: str) -> bytes:
        """Fetch image data from URL with browser-like headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            # Convert URL if needed (e.g. Google Drive)
            direct_url = self.url_converter.convert_url(image_url)
            if not direct_url:
                raise ValueError(f"Could not convert URL: {image_url}")
                
            logger.debug(f"Fetching image from: {direct_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(direct_url, headers=headers) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to fetch image: HTTP {response.status}")
                    return await response.read()
                    
        except Exception as e:
            logger.error(f"Error fetching image from {image_url}: {str(e)}")
            raise
            
    async def analyze_image(
        self,
        image_url: str,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Analyze an image using Gemini"""
        try:
            # Fetch image data
            image_data = await self._fetch_image(image_url)
            
            # Create content parts
            content = [
                {"text": prompt},
                {"mime_type": "image/jpeg", "data": image_data}
            ]
            
            logger.debug(f"Sending prompt: {prompt[:200]}...")
            logger.debug(f"Image data size: {len(image_data)} bytes")
            
            # Configure the model
            response = self.model.generate_content(
                contents=content,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    top_p=0.99,
                    top_k=10,
                    max_output_tokens=2048,
                    candidate_count=1
                ),
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_ONLY_HIGH"
                    }
                ],
                stream=True
            )
            
            # Collect response chunks
            chunks = []
            for chunk in response:
                if chunk.text:
                    chunks.append(chunk.text)
                    logger.debug(f"Received chunk: {chunk.text[:100]}...")
            
            # Process chunks into JSON if requested
            if expect_json:
                return self._process_json_stream(chunks)
            
            # Otherwise return raw text
            return ''.join(chunks)
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            raise
            
    async def generate(
        self,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Generate text using Gemini"""
        try:
            # Generate content with streaming
            response = self.model.generate_content(prompt, stream=True)
            
            # Collect response chunks
            chunks = []
            for chunk in response:
                if chunk.text:
                    chunks.append(chunk.text)
                    logger.debug(f"Received chunk: {chunk.text[:100]}...")
            
            # Process chunks into JSON if requested
            if expect_json:
                return self._process_json_stream(chunks)
            
            # Otherwise return raw text
            return ''.join(chunks)
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            raise
