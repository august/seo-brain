"""Image analysis service using vision LLMs"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

from utils.llm_base import LLMProvider
from utils.llm_factory import LLMFactory

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Image Analysis Service",
    description="Analyze product images using vision LLMs",
    version="1.0.0"
)

class Platform(str, Enum):
    """Supported platforms"""
    ALL = "all"

class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis"""
    image_urls: List[str]
    context: Optional[Dict[str, Any]] = None
    platform: Optional[str] = None

class ImageAnalyzer:
    """Analyze product images using vision LLMs"""
    
    def _validate_json(self, data: Dict[str, Any]) -> bool:
        """Validate that we have a complete JSON structure"""
        required_sections = [
            'nlp_analysis',
            'long_tail_opportunities',
            'answer_engine_optimization'
        ]
        
        # Check for required top-level sections
        missing = [key for key in required_sections if key not in data]
        if missing:
            logger.warning(f"Missing required sections: {missing}")
            return False
            
        # Check for required nested structures
        validation_score = 0
        max_score = 3  # One point for each main section being mostly complete
        
        if 'nlp_analysis' in data:
            required_nlp = ['semantic_clusters', 'linguistic_patterns', 'query_intent_analysis', 'sentiment_mapping']
            present = sum(1 for key in required_nlp if key in data['nlp_analysis'])
            if present >= len(required_nlp) * 0.75:  # 75% of required subsections
                validation_score += 1
            else:
                logger.warning(f"NLP analysis missing too many sections: {[key for key in required_nlp if key not in data['nlp_analysis']]}")
                
        if 'long_tail_opportunities' in data:
            required_tail = ['specific_features', 'use_case_variations', 'modifier_combinations']
            present = sum(1 for key in required_tail if key in data['long_tail_opportunities'])
            if present >= len(required_tail) * 0.75:
                validation_score += 1
            else:
                logger.warning(f"Long tail missing too many sections: {[key for key in required_tail if key not in data['long_tail_opportunities']]}")
                
        if 'answer_engine_optimization' in data:
            required_aeo = ['featured_snippet_opportunities', 'knowledge_panel_signals', 'rich_result_patterns']
            present = sum(1 for key in required_aeo if key in data['answer_engine_optimization'])
            if present >= len(required_aeo) * 0.66:  # 66% for AEO since it's less critical
                validation_score += 1
            else:
                logger.warning(f"AEO missing sections: {[key for key in required_aeo if key not in data['answer_engine_optimization']]}")
        
        # Return true if we have at least 2 out of 3 sections mostly complete
        return validation_score >= 2
                
        return True
    
    def __init__(self):
        """Initialize the ImageAnalyzer"""
        self.llm = LLMFactory.create(LLMProvider.GEMINI)
        
        # Load the prompt template
        prompts_dir = Path(__file__).parent.parent / "prompts"
        self.analysis_prompt = self._load_prompt(prompts_dir / "image_analysis_prompt.md")
        
        logger.info("ImageAnalyzer initialized")
        
    def _load_prompt(self, path: Path) -> str:
        """Load a prompt template from file"""
        if not path.exists():
            logger.warning(f"Prompt file not found: {path}, using default")
            return "Please analyze this image in detail."
            
        with open(path, 'r') as f:
            return f.read()
        
    def set_llm_provider(self, provider: LLMProvider, api_key: Optional[str] = None) -> None:
        """Change LLM provider"""
        self.llm = LLMFactory.create(provider, api_key)
        
    async def analyze(self, request: ImageAnalysisRequest) -> Dict[str, Any]:
        """Analyze product images"""
        try:
            if not request.image_urls:
                return {
                    "analyses": [],
                    "summary": {
                        "has_images": False,
                        "message": "No images provided for analysis"
                    }
                }
                
            results = []
            for url in request.image_urls:
                analysis = await self._analyze_single_image(
                    url,
                    context=request.context or {},
                    platform=request.platform
                )
                results.append(analysis)
                
            # For now, we'll skip the summary for multiple images
            # since our new structure is much more comprehensive
            return {
                "analyses": results,
                "summary": {
                    "common_themes": {
                        "strengths": ["See individual analyses"],
                        "areas_for_improvement": ["See individual analyses"]
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
            
    def _clean_json_string(self, json_str: str) -> str:
        """Clean and normalize JSON string for parsing."""
        # Remove any potential Unicode BOM and whitespace
        json_str = json_str.strip().lstrip('\ufeff')
        
        # Remove any trailing commas before closing braces/brackets
        json_str = re.sub(r',\s*([\]\}])', r'\1', json_str)
        
        # Handle potential line breaks in strings
        json_str = json_str.replace('\n', '\\n')
        
        # Fix common JSON formatting issues
        json_str = re.sub(r'\s+', ' ', json_str)  # Normalize whitespace
        json_str = re.sub(r',\s*,', ',', json_str)  # Fix double commas
        json_str = re.sub(r'\}\s*\{', '},{', json_str)  # Fix adjacent objects
        json_str = re.sub(r'\]\s*\[', '],[', json_str)  # Fix adjacent arrays
        
        # Balance quotes
        quote_count = json_str.count('"')
        if quote_count % 2 == 1:  # Odd number of quotes
            json_str = json_str.rstrip('"')  # Remove trailing quote if present
        
        return json_str
        
    async def _analyze_single_image(
        self,
        image_url: str,
        context: Dict[str, Any],
        platform: Optional[str]
    ) -> Dict[str, Any]:
        """Analyze a single product image"""
        try:
            logger.info(f"Starting analysis of image: {image_url}")
            logger.info(f"Context: {context}")
            if platform:
                logger.info(f"Platform: {platform}")

            # Build prompt with context
            prompt = self.analysis_prompt
            for key in ['description', 'occasion', 'platform', 'personalized', 'voice']:
                placeholder = "${" + key + "}"
                value = context.get(key, "Not specified")
                prompt = prompt.replace(placeholder, value)
            logger.info("Prompt template prepared")
            
            # Analyze image with retries and validation
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    logger.info(f"Starting analysis attempt {attempt + 1} of {max_retries}")
                    
                    # Get response from LLM with streaming
                    logger.info("Sending request to Gemini...")
                    response_buffer = []
                    async for chunk in self.llm.analyze_image_stream(
                        image_url=image_url,
                        prompt=prompt,
                        expect_json=True
                    ):
                        if isinstance(chunk, str):
                            response_buffer.append(chunk)
                        elif isinstance(chunk, dict):
                            response = chunk
                            break
                    
                    # If we got string chunks, combine and parse
                    if response_buffer:
                        raw_response = ''.join(response_buffer)
                        logger.info("Received complete response from Gemini")
                        cleaned_json = self._clean_json_string(raw_response)
                        response = self.llm.parse_json(cleaned_json)
                    logger.info("JSON parsed successfully")
                    
                    # Validate JSON structure
                    logger.info("Validating response structure...")
                    if not self._validate_json(response):
                        logger.warning(
                            f"Invalid JSON structure on attempt {attempt + 1}. "
                            f"Missing sections: {[k for k in ['nlp_analysis', 'long_tail_opportunities', 'answer_engine_optimization'] if k not in response]}"
                        )
                        if attempt == max_retries - 1:
                            return {
                                'status': 'error',
                                'error_message': 'Failed to generate valid JSON structure after all retries',
                                'image_url': image_url
                            }
                        continue
                        
                    logger.info("✨ Analysis completed successfully!")
                    logger.info(f"Response sections: {list(response.keys())}")
                    return response
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"❌ All {max_retries} attempts failed. Last error: {str(e)}")
                        return {
                            'status': 'error',
                            'error_message': f'Failed after {max_retries} attempts: {str(e)}',
                            'image_url': image_url
                        }
                    logger.warning(f"⚠️ Attempt {attempt + 1} failed: {str(e)}. Retrying...")
                    continue
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze image {image_url}: {str(e)}")
            raise
            
# Initialize analyzer
analyzer = ImageAnalyzer()

@app.post("/analyze")
async def analyze_images(request: ImageAnalysisRequest) -> Dict[str, Any]:
    """Analyze product images"""
    return await analyzer.analyze(request)