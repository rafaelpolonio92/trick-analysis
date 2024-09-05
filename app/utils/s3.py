import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = "video-trick-analysis"

def download_video_from_s3(video_url: str) -> str:
    local_path = "/tmp/video.mp4"
    s3_client.download_file(BUCKET_NAME, video_url, local_path)
    return local_path
