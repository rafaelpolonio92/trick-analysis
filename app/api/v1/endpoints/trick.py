from fastapi import APIRouter, HTTPException
from app.schemas.trick import TrickAnalysisRequest, TrickAnalysisResponse
from app.services.trick_analysis_service import analyze_trick

router = APIRouter()

@router.post("/analyze", response_model=TrickAnalysisResponse)
async def analyze_trick_route(request: TrickAnalysisRequest):
    try:
        result = await analyze_trick(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
