import asyncio
import logging
from utils.llm_gemini import GeminiClient

# Configure logging
logging.basicConfig(level=logging.DEBUG)

async def test_image_analysis():
    # Initialize client
    client = GeminiClient()
    
    # Test image URL (Google Drive)
    image_url = "https://drive.google.com/open?id=1ZKWCBLpA91cOK0kw6NbPm8q9tk8V9fL5&usp=drive_fs"
    
    # Load prompt
    with open('prompts/image_analysis_prompt.md', 'r') as f:
        prompt = f.read()
    
    # Replace placeholders
    prompt = prompt.replace('${platform}', 'Amazon')
    prompt = prompt.replace('${product_description}', 'High-end coffee maker')
    
    try:
        # Analyze image
        result = await client.analyze_image(
            image_url=image_url,
            prompt=prompt,
            expect_json=True
        )
        
        print("\n=== Analysis Result ===")
        print(f"Got result of type: {type(result)}")
        if isinstance(result, dict):
            print("\nKeys found:")
            for key in result.keys():
                print(f"- {key}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_image_analysis())
