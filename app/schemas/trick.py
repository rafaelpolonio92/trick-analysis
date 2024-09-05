from pydantic import BaseModel

class TrickAnalysisRequest(BaseModel):
    user_id: str
    trick_id: str
    video_url: str

class TrickAnalysisResponse(BaseModel):
    status: str
    message: str
