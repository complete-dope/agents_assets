# Collection of all response formats 

from pydantic import BaseModel
from typing import List , Literal , Dict, Optional


class HighLevelStep(BaseModel):
    action: str
    target: str
    description: Optional[str] = None

class HighLevelStepsOutput(BaseModel):
    steps: List[HighLevelStep]


    