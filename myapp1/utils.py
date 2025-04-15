from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.agent import AgentRunResult
import os
import mimetypes
import logging
if __name__ == "__main__":
    from schemas import CaptionOption, CaptionResponse
else:
    from .schemas import CaptionOption, CaptionResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimAgent:
    def __init__(self):
        self.model = GeminiModel(
            "gemini-2.0-flash",
            provider=GoogleGLAProvider(api_key=os.getenv("GEMINI_API_KEY")),
        )
        

    def generate_caption(
            self,
            image_data: bytes,
            platform: str = "instagram",
            file_name: str = None,
            num_options: int = 3
    ) -> CaptionResponse:
        """
        Generate multiple caption options for an image.
        
        Args:
            image_data: Raw image data bytes (direct from upload)
            platform: Social media platform (instagram, twitter, etc.)
            file_name: Original filename (optional, for MIME type detection)
            num_options: Number of different caption options to generate
            
        Returns:
            CaptionResponse object with multiple caption options
        """
        try:
            # Determine the MIME type based on file name or default to image/jpeg
            media_type = 'image/jpeg'  # Default fallback
            if file_name:
                guessed_type = mimetypes.guess_type(file_name)[0]
                if guessed_type:
                    media_type = guessed_type
                    
            logger.info(f"Processing image with media type: {media_type}")
            
            # Create a single prompt that asks for multiple captions in one call
            # This approach is more efficient than making multiple API calls
            agent = Agent(
                self.model,
                result_type=CaptionResponse,  # Changed to expect CaptionResponse directly
                system_prompt = f"""
                Create {num_options} distinct caption options for this image for use on {platform}.
                
                For each caption option:
                1. Write a unique and engaging caption text
                2. Include 3-5 relevant hashtags as a list
                3. Specify an emotional tone (e.g., enthusiastic, reflective, humorous)
                
                Make each option different in style and approach to give the user meaningful choices.
                Return the results as a list of options, each with caption text, hashtags, and tone.
                """ 
            )
            
            # Create a BinaryContent object with the raw image data
            image_content = BinaryContent(data=image_data, media_type=media_type)
            
            # Make a single call to the model to generate all caption options at once
            logger.info("Calling AI model to generate caption options")
            response = agent.run_sync(
                [
                    image_content,
                ]
            )
            
            logger.info(f"Agent result type: {type(response)}")

            return response.data
            
            
                
        except Exception as e:
            logger.error(f"Error generating captions: {str(e)}")
            # Create a fallback response in case of errors
            fallback_option = CaptionOption(
                caption="Check out this amazing image!",
                hashtags=["#photo", "#share", f"#{platform}"],
                tone="neutral"
            )
            return CaptionResponse(options=[fallback_option])
