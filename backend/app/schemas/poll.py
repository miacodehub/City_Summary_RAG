from typing import Optional
from pydantic import BaseModel

class LocationRequest(BaseModel):
    name: str
    current_city: str
    preference: Optional[str] = ""