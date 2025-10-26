import os
from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.utils.config import AWS_DEFAULT_REGION, S3_BUCKET_NAME


_s3_client = None


def get_s3_client():
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=AWS_DEFAULT_REGION)
    return _s3_client


def download_video_from_s3(object_key: str, local_path: Optional[str] = None, bucket_name: Optional[str] = None) -> str:
    client = get_s3_client()
    resolved_bucket = bucket_name or S3_BUCKET_NAME
    resolved_local_path = local_path or "/tmp/video.mp4"
    try:
        client.download_file(resolved_bucket, object_key, resolved_local_path)
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to download s3://{resolved_bucket}/{object_key}: {e}")
    return resolved_local_path


def upload_csv_to_s3(file_path: str, user_id: str, s3_bucket_name: Optional[str] = None) -> str:
    """Uploads the CSV file to an S3 bucket under a folder named after the user ID.

    Returns the S3 key of the uploaded object.
    """
    client = get_s3_client()
    bucket = s3_bucket_name or S3_BUCKET_NAME
    s3_key = f"{user_id}/{os.path.basename(file_path)}"
    try:
        client.upload_file(file_path, bucket, s3_key)
        print(f"File {file_path} uploaded to s3://{bucket}/{s3_key}")
        return s3_key
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Error uploading {file_path} to s3://{bucket}/{s3_key}: {e}")


def generate_presigned_url(object_key: str, bucket_name: Optional[str] = None, expiration: int = 3600) -> str:
    """Generate a pre-signed URL for an S3 object."""
    client = get_s3_client()
    bucket = bucket_name or S3_BUCKET_NAME
    try:
        response = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiration,
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Error generating pre-signed URL for s3://{bucket}/{object_key}: {e}")
    return response