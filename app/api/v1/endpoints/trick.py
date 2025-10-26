import os
from fastapi import APIRouter, HTTPException
from app.schemas.trick import TrickAnalysisRequest, TrickAnalysisResponse
from app.services.trick_analysis_service import analyze_trick, save_trick_model_to_csv, combine_csv_with_label
from app.scripts.trick_analysis_model import train_lstm_model;

router = APIRouter()

@router.post("/analyze", response_model=TrickAnalysisResponse)
async def analyze_trick_route(request: TrickAnalysisRequest):
    try:
        result = await analyze_trick(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/train")
async def train_model_route(request: TrickAnalysisRequest):
    try:
        await save_trick_model_to_csv("videos")
        df = combine_csv_with_label("videos", "perfect_ollie")
        df.to_csv("ollie_dataset.csv", index=False)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train-lstm-model")
async def train_model_endpoint():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

    # Construct the dataset path safely
    dataset_path = os.path.join(root_dir, "ollie_dataset.csv")
    try:
        # Call the train_lstm_model function to trigger training
        result = train_lstm_model(dataset_path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during training: {str(e)}")