import os


def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


# AWS / S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "video-trick-analysis")


# Paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK_DIR = os.getenv("WORK_DIR", "/tmp")
VIDEOS_DIR = os.getenv("VIDEOS_DIR", os.path.join(PROJECT_ROOT, "videos"))
DATASET_PATH = os.getenv("DATASET_PATH", os.path.join(PROJECT_ROOT, "ollie_dataset.csv"))
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(PROJECT_ROOT, "trick_analysis_model.h5"))


# Runtime tuning
MEDIAPIPE_STATIC_IMAGE_MODE = os.getenv("MEDIAPIPE_STATIC_IMAGE_MODE", "0") == "1"
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = float(os.getenv("MEDIAPIPE_MIN_DETECTION_CONFIDENCE", "0.5"))
MEDIAPIPE_MIN_TRACKING_CONFIDENCE = float(os.getenv("MEDIAPIPE_MIN_TRACKING_CONFIDENCE", "0.5"))


