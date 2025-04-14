from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.agent import AgentRunResult
import os
import mimetypes
if __name__ == "__main__":
    from schemas import Caption
else:
    from .schemas import Caption


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
            # include_hashtags: bool = True
    ) -> Caption:
        """
        Generate an appropriate caption for an image.
        
        Args:
            image_data: Raw image data bytes (direct from upload)
            platform: Social media platform (instagram, twitter, etc.)
            file_name: Original filename (optional, for MIME type detection)
            
        Returns:
            Caption object with text and hashtags
        """
        # Determine the MIME type based on file name or default to image/jpeg
        media_type = 'image/jpeg'  # Default fallback
        if file_name:
            guessed_type = mimetypes.guess_type(file_name)[0]
            if guessed_type:
                media_type = guessed_type
        
        agent = Agent(
            self.model,
            result_type=Caption,
            system_prompt = f"""
            Create an engaging caption for this image for {platform}.
            Analyze the image content and create a caption that's relevant to what's shown.
            Also suggest 3-5 relevant hashtags.
            """ 
        )
        
        # Create a BinaryContent object with the raw image data
        image_content = BinaryContent(data=image_data, media_type=media_type)
        
        # Run the agent with the image content
        agent_result = agent.run_sync(
            [
                image_content,
            ]
        )
        
        return agent_result.data
