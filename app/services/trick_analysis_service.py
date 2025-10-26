import cv2
from app.schemas.trick import TrickAnalysisRequest, TrickAnalysisResponse
import mediapipe as mp
import os
import aiohttp
import csv
from fastapi import HTTPException
from app.utils.s3 import upload_csv_to_s3
import pandas as pd

BUCKET_NAME = "video-trick-analysis"
output_csv = "pose_data.csv"
user_id = "user123"
trick_video_path = "/videos"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def extract_pose_data(video_path: str, output_csv: str):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    print("Processing video...")
    if not cap.isOpened():
        raise Exception("Error opening video file")
    
    with open(output_csv, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        # Write header
        header = ['frame'] + [f'{joint}_{axis}' for joint in range(33) for axis in ['x', 'y', 'z', 'visibility']]
        csv_writer.writerow(header)

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB as MediaPipe processes RGB images
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform pose detection
            result = pose.process(image_rgb)

            # If pose landmarks are detected, save them to CSV
            if result.pose_landmarks:
                row = [frame_count]
                for landmark in result.pose_landmarks.landmark:
                    row.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                csv_writer.writerow(row)

            frame_count += 1

    cap.release()

async def save_trick_model_to_csv(trick_video_path):
    for video_file in os.listdir(trick_video_path):
        if video_file.endswith(".mp4"):
            video_path = os.path.join(trick_video_path, video_file)
            output_csv = os.path.join(trick_video_path, video_file.replace('.mp4', '_pose.csv'))
            extract_pose_data(video_path, output_csv)
            print(f"Extracted pose data for {video_file} into {output_csv}")

def combine_csv_with_label(videos_path, label):
    combined_data = []

    for csv_file in os.listdir(videos_path):
        if csv_file.endswith("_pose.csv"):
            csv_path = os.path.join(videos_path, csv_file)
            df = pd.read_csv(csv_path)
            df['label'] = label
            combined_data.append(df)

    # Combine all data into a single DataFrame
    combined_df = pd.concat(combined_data, ignore_index=True)
    return combined_df

async def analyze_trick(request: TrickAnalysisRequest) -> TrickAnalysisResponse:
    try:
        video_path = "/tmp/video.mp4"
        csv_file_path = "/tmp/pose_data.csv"
        
        # Download the video using an asynchronous HTTP request
        async with aiohttp.ClientSession() as session:
            async with session.get(request.video_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Error downloading video")
                video_content = await response.read()
                print("Video downloaded successfully")

        # Write video to a temporary file
        with open(video_path, 'wb') as f:
            f.write(video_content)
            print("Video saved to disk")

        # Extract pose data from the video
        extract_pose_data(video_path, csv_file_path)
       
        # Upload the CSV to S3
        upload_csv_to_s3(csv_file_path, user_id, BUCKET_NAME)

        # Clean up video and CSV file
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)

        return TrickAnalysisResponse(status="success", message="Trick analysis completed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing trick: {e}")
