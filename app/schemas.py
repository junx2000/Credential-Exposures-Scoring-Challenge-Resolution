from pydantic import BaseModel
class UserScoreResponse(BaseModel):
    email: str
    score: int