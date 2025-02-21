# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import re
import datetime
import asyncio
from utils.url_converter import URLConverter
from analyzers.image_analyzer import ImageAnalyzer

app = FastAPI(
    title="Product SEO Optimizer",
    description="Optimize product listings with AI-powered image and text analysis",
    version="1.0.0"
)

class ProductOptimizeRequest(BaseModel):
    """Request model for product optimization"""
    description: str
    image_url: str
    occasion: str = "general"
    personalized: str = ""
    platform: str = "Etsy"
    callback_url: Optional[str] = None
    voice: Optional[str] = None

@app.post('/api/v1/product/seo-optimize')
async def seo_optimize_product(request: ProductOptimizeRequest):
    """
    API endpoint to receive product data, analyze it, and return SEO-optimized results.
    Performs comprehensive image and text analysis to generate optimized content.
    """
    print(f"Received request: {request.dict()}")
    try:
        # Step 1: Image Analysis (Primary Analysis)
        image_analysis = await analyze_image(
            image_url=request.image_url,
            description=request.description,
            occasion=request.occasion,
            platform=request.platform,
            personalized=request.personalized,
            voice=request.voice
        )
        
        # Check for analysis error
        if isinstance(image_analysis, dict) and image_analysis.get('status') == 'error':
            raise HTTPException(
                status_code=500,
                detail={
                    'error_type': 'image_analysis_error',
                    'error_message': image_analysis.get('error_message', 'Unknown error'),
                    'image_url': image_analysis.get('image_url')
                }
            )

        # Prepare context for subsequent analyses
        analysis_context = {
            'image_analysis': image_analysis['image_analysis'],
            'request_params': {
                'description': request.description,
                'personalized': request.personalized,
                'platform': request.platform,
                'occasion': request.occasion,
                'voice': request.voice
            },
            'timestamp': datetime.datetime.now().isoformat(),
            'api_version': '2.0'
        }

        # Step 2: Secondary Analyses (using image analysis results)
        # These will be enhanced later with their own analyzers
        text_analysis = analyze_text(request.description)
        opt_title = generate_optimized_title(request.dict(), analysis_context)
        opt_description = generate_optimized_description(request.dict(), analysis_context)
        opt_tags = generate_optimized_tags(request.dict(), analysis_context)

        # Combine all analyses
        response_data = {
            'status': 'success',
            'optimized_content': {
                'title': opt_title,
                'description': opt_description,
                'tags': opt_tags
            },
            'analysis_summary': {
                'text_analysis': text_analysis,
                'image_analysis': image_analysis['image_analysis']
            },
            'context': analysis_context
        }

        # Handle webhook callback if provided
        if request.callback_url:
            await send_webhook_callback(request.callback_url, response_data)

        return response_data
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                'error_type': 'processing_error',
                'error_message': str(e)
            }
        )
        raise HTTPException(
            status_code=500,
            detail={
                'error_type': 'processing_error',
                'error_message': str(e)
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'error_type': 'system_error',
                'error_message': f"An unexpected error occurred: {str(e)}"
            }
        )


# Initialize global analyzer instance
image_analyzer = ImageAnalyzer()

async def analyze_image(image_url, description=None, occasion="general", platform="Etsy", personalized="", voice=None):
    """Analyze an image URL using our comprehensive image analysis system.
    
    Args:
        image_url (str): URL of the image to analyze
        
    Returns:
        dict: Analysis results with visual, market, and psychological insights
        
    Raises:
        ValueError: If URL conversion fails
        RuntimeError: If image analysis fails
    """
    print(f"Analyzing image from URL: {image_url}")

    # Convert URL to direct download URL
    url_converter = URLConverter()
    direct_url = url_converter.convert_url(image_url)
    
    if not direct_url:
        raise ValueError(f"Could not convert URL to direct download URL: {image_url}")

    print(f"Using direct download URL: {direct_url}")

    try:
        # Get comprehensive image analysis
        analysis_results = await image_analyzer._analyze_single_image(
            image_url=direct_url,
            context={
                'description': description,
                'occasion': occasion,
                'personalized': personalized,
                'platform': platform,
                'voice': voice
            },
            platform=platform
        )
        
        # If we got an error response, return it
        if isinstance(analysis_results, dict) and analysis_results.get('status') == 'error':
            return analysis_results
            
        # Add metadata about the analysis
        analysis_results['metadata'] = {
            'original_url': image_url,
            'direct_url': direct_url,
            'analysis_version': '2.0',
            'analysis_timestamp': datetime.datetime.now().isoformat()
        }
        
        return {
            'status': 'success',
            'image_analysis': analysis_results
        }
        
    except Exception as e:
        print(f"Error analyzing image: {str(e)}")
        return {
            'status': 'error',
            'error_message': str(e),
            'image_url': direct_url
        }


def analyze_text(description):
    print(f"Placeholder: Analyzing text description: {description}")
    return {"text_analysis": "Placeholder Text Analysis Keywords"} # Placeholder data

def generate_optimized_title(product_data, analysis_results):
    print("Placeholder: Generating optimized title")
    return "Placeholder Optimized Title" # Placeholder title

def generate_optimized_description(product_data, analysis_results):
    print("Placeholder: Generating optimized description")
    return "Placeholder Optimized Description" # Placeholder description

def generate_optimized_tags(product_data, analysis_results):
    print("Placeholder: Generating optimized tags")
    return ["placeholder", "tags"] # Placeholder tags

def create_analysis_summary(analysis_results):
    print("Placeholder: Creating analysis summary")
    return {"summary": "Placeholder Analysis Summary"} # Placeholder summary

def send_webhook_callback(callback_url, response_data):
    print(f"Placeholder: Sending webhook callback to: {callback_url} with data: {response_data}")
    # In a real implementation, you'd use a library like 'requests' to make an actual HTTP POST request


def analyze_text(description: str) -> Dict[str, Any]:
    """Analyze text content of the product description."""
    return {
        'text_analysis': 'Basic text analysis will be implemented here'
    }

def generate_optimized_title(params: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Generate an optimized title using image and text analysis context."""
    return f"Optimized title for {params['description']} (Using {context['request_params']['occasion']} context)"

def generate_optimized_description(params: Dict[str, Any], context: Dict[str, Any]) -> str:
    """Generate an optimized description using image and text analysis context."""
    return f"Optimized description for {params['description']} (Using {context['request_params']['occasion']} context)"

def generate_optimized_tags(params: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
    """Generate optimized tags using image and text analysis context."""
    return [params['occasion'], context['request_params']['platform'], "test_tag"]

async def send_webhook_callback(url: str, data: Dict[str, Any]) -> None:
    """Send analysis results to the specified webhook URL."""
    print(f"Would send webhook to {url} with data: {data}")

if __name__ == '__main__':
    import uvicorn
    import argparse
    import sys
    from pathlib import Path
    
    # Add the project root to Python path
    project_root = str(Path(__file__).parent.absolute())
    if project_root not in sys.path:
        sys.path.append(project_root)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    
    print(f"FastAPI app starting in development mode on port {args.port}...")
    uvicorn.run("app:app", host="127.0.0.1", port=args.port, reload=True)