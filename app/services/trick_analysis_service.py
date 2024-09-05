import boto3
import cv2
from app.schemas.trick import TrickAnalysisRequest, TrickAnalysisResponse
import requests

# Initialize the S3 client
s3_client = boto3.client('s3')

BUCKET_NAME = "video-trick-analysis"

# def generate_presigned_url(bucket_name: str, object_key: str, expiration=3600) -> str:
#     """Generate a pre-signed URL for an S3 object."""
#     try:
#         response = s3_client.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': bucket_name, 'Key': object_key},
#             ExpiresIn=expiration
#         )
#     except Exception as e:
#         raise Exception(f"Error generating pre-signed URL: {e}")
    
#     return response

async def analyze_trick(request: TrickAnalysisRequest) -> TrickAnalysisResponse:
    try:
        # Download the video using the pre-signed URL
        video_path = "/tmp/video.mp4"
        response = requests.get(request.video_url)
        print(response)
        with open(video_path, 'wb') as f:
            f.write(response.content)

        # Process video (example processing logic)
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Error opening video file")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            print(frame)
            # Your trick analysis logic here

        cap.release()

        return TrickAnalysisResponse(status="success", message="Trick analysis completed")

    except Exception as e:
        raise Exception(f"Error analyzing trick: {e}")
