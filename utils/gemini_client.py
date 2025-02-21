"""Gemini LLM client implementation"""
import json
import logging
from typing import Dict, Any, Union, AsyncGenerator
import aiohttp
import google.generativeai as genai
from google.generativeai.types import content_types

from .llm_base import BaseLLMClient

logger = logging.getLogger(__name__)

class GeminiClient(BaseLLMClient):
    """Client for Google's Gemini API"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro-vision')
        
    def parse_json(self, text: str) -> Dict[str, Any]:
        """Parse JSON from text, with error handling"""
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            raise
            
    async def analyze_image(
        self,
        image_url: str,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        timeout = 30.0  # 30 second default timeout
        """Analyze an image using Gemini"""
        try:
            # Download image with timeout
            timeout_client = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout_client) as session:
                async with session.get(image_url) as response:
                    image_data = await response.read()
                    
            # Convert to Gemini image format
            image = content_types.ImageContent.from_bytes(image_data)
            
            # Get response
            response = await self.model.generate_content_async(
                contents=[prompt, image],
                generation_config={"temperature": 0.7}
            )
            
            text = response.text
            if expect_json:
                return self.parse_json(text)
            return text
            
        except Exception as e:
            logger.error(f"Gemini image analysis failed: {str(e)}")
            raise
            
    async def analyze_image_stream(
        self,
        image_url: str,
        prompt: str,
        expect_json: bool = False
    ) -> AsyncGenerator[Union[str, Dict[str, Any]], None]:
        timeout = 30.0  # 30 second default timeout
        """Stream image analysis results from Gemini"""
        try:
            # Download image with timeout
            timeout_client = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(timeout=timeout_client) as session:
                async with session.get(image_url) as response:
                    image_data = await response.read()
                    
            # Convert to Gemini image format
            image = content_types.ImageContent.from_bytes(image_data)
            
            # Get streaming response with timeout
            import asyncio
            try:
                response = await asyncio.wait_for(
                    self.model.generate_content_async(
                        contents=[prompt, image],
                        generation_config={"temperature": 0.7},
                        stream=True
                    ),
                    timeout=timeout
                )
            
            # Stream chunks with safety limits
            MAX_BUFFER_SIZE = 1024 * 1024  # 1MB limit
            MAX_CHUNKS = 1000  # Maximum number of chunks to process
            CHUNK_TIMEOUT = 5.0  # 5 second timeout per chunk
            
            buffer = []
            buffer_size = 0
            chunk_count = 0
            last_progress = 0  # Track last successful parse attempt
            
            async for chunk in response:
                try:
                    # Apply timeout per chunk
                    chunk = await asyncio.wait_for(anext(response.__aiter__()), CHUNK_TIMEOUT)
                    chunk_count += 1
                    if chunk_count > MAX_CHUNKS:
                    logger.error(f"Exceeded maximum chunk count: {MAX_CHUNKS}")
                    raise ValueError(f"Response exceeded {MAX_CHUNKS} chunks")
                    
                if chunk.text:
                    chunk_size = len(chunk.text.encode('utf-8'))
                    if buffer_size + chunk_size > MAX_BUFFER_SIZE:
                        logger.error(f"Buffer would exceed size limit: {MAX_BUFFER_SIZE} bytes")
                        raise ValueError(f"Response would exceed {MAX_BUFFER_SIZE} bytes")
                        
                    buffer.append(chunk.text)
                    buffer_size += chunk_size
                    
                    if expect_json:
                        try:
                            complete_text = ''.join(buffer)
                            json_response = self.parse_json(complete_text)
                            yield json_response
                            # Success! Clear buffer
                            buffer = []
                            buffer_size = 0
                            last_progress = chunk_count
                        except json.JSONDecodeError:
                            # Check if we're making progress
                            if chunk_count - last_progress > 100:
                                logger.error("No parsing progress in last 100 chunks")
                                raise ValueError("Failed to make progress parsing JSON")
                            continue
                    else:
                        yield chunk.text
                        
            # Yield any remaining buffer content
            if buffer and expect_json:
                try:
                    complete_text = ''.join(buffer)
                    json_response = self.parse_json(complete_text)
                    yield json_response
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse final buffer: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Gemini streaming image analysis failed: {str(e)}")
            raise
            
    async def generate(
        self,
        prompt: str,
        expect_json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Generate text using Gemini"""
        try:
            response = await self.model.generate_content_async(
                contents=prompt,
                generation_config={"temperature": 0.7}
            )
            
            text = response.text
            if expect_json:
                return self.parse_json(text)
            return text
            
        except Exception as e:
            logger.error(f"Gemini text generation failed: {str(e)}")
            raise
