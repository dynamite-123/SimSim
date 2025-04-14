from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import SimAgent


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def generate_caption(request):
    """
    API endpoint for generating captions for images.
    
    POST request with:
        - image: Image file (required)
        - platform: Social media platform (optional, defaults to "instagram")
    """
    try:
        # Check if an image file was provided
        if 'image' not in request.FILES:
            return Response(
                {"error": "No image provided. Please upload an image."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get image data
        image_file = request.FILES['image']
        image_data = image_file.read()
        file_name = image_file.name
        
        # Get optional platform parameter
        platform = request.data.get('platform', 'instagram')
    
        # Initialize the AI agent
        sim_agent = SimAgent()
        
        # Generate caption
        caption_result = sim_agent.generate_caption(
            image_data=image_data,
            platform=platform,
            file_name=file_name
        )
        
        # Convert the Pydantic object to a JSON-compatible dictionary
        result_json = caption_result.model_dump(mode="json")
        
        # Return the properly converted JSON
        return Response(
            result_json,
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": f"Caption generation failed: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
