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
