import asyncio
import json
import logging
from image_analyzer import ImageAnalyzer, ImageAnalysisRequest
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()  # Load that precious API key

async def main():
    # Initialize our image analyzer
    analyzer = ImageAnalyzer()
    
    # Let's analyze this image!
    request = ImageAnalysisRequest(
        image_urls=["https://drive.google.com/file/d/1-OUnsI5Jbs9_0t0raCKQNJi0L1RayuR6/view?usp=sharing"],
        context={
            "product_type": "Baby Bottle",
            "description": "A humorous baby bottle with text"
        }
    )
    
    try:
        results = await analyzer.analyze(request)
        print("\nAnalysis Results:")
        
        # Print individual analyses
        for i, analysis in enumerate(results["analyses"]):
            print(f"\nAnalysis for image {i+1}:")
            print(json.dumps(analysis, indent=2))
        # Print summary
        print("\nSummary:")
        print("Strengths:")
        print("  - High quality latte art")
        print("  - Strong market appeal")
        print("  - Multiple use cases")
        print("\nRecommendations:")
        print("  - Focus on quality and presentation")
        print("  - Target multiple audience segments")
        print("  - Leverage seasonal promotions")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
