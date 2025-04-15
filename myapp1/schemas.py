# import google.generativeai as genai
from pydantic import BaseModel
from typing import List

class Caption(BaseModel):
    """
    Schema for image caption generation response.
    
    Attributes:
        caption: The main caption text for the image
        hashtags: A list of relevant hashtags for the image
        tone: The emotional tone of the caption
    """
    caption: str
    hashtags: List[str] = []
    tone: str = "neutral"
    
    class Config:
        json_schema_extra = {
            "example": {
                "caption": "Enjoying the sunset vibes at the beach. Perfect end to a perfect day!",
                "hashtags": ["#sunset", "#beachlife", "#naturelover", "#peacefulmoments"],
                "tone": "relaxed"
            }
        }

class CaptionOption(BaseModel):
    """
    Schema for a single caption option.
    
    Attributes:
        caption: The main caption text for the image
        hashtags: A list of relevant hashtags for the image
        tone: The emotional tone of the caption
    """
    caption: str
    hashtags: List[str] = []
    tone: str = "neutral"

class CaptionResponse(BaseModel):
    """
    Schema for image caption generation response with multiple options.
    
    Attributes:
        options: A list of caption options for the user to choose from
    """
    options: List[CaptionOption] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "options": [
                    {
                        "caption": "Enjoying the sunset vibes at the beach. Perfect end to a perfect day!",
                        "hashtags": ["#sunset", "#beachlife", "#naturelover", "#peacefulmoments"],
                        "tone": "relaxed"
                    },
                    {
                        "caption": "Golden hour magic by the ocean. Nature's best light show!",
                        "hashtags": ["#goldenhour", "#oceanviews", "#sunsetlovers", "#eveningvibes"],
                        "tone": "enthusiastic"
                    },
                    {
                        "caption": "Finding peace where the land meets the sea. Simple moments, profound joy.",
                        "hashtags": ["#mindfulness", "#coastallife", "#eveningwalk", "#gratitude"],
                        "tone": "reflective"
                    }
                ]
            }
        }
