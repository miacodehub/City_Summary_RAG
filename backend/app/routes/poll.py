from fastapi import APIRouter
from app.schemas.poll import LocationRequest
from app.rag.generation import generate_summary
from app.services.travel import get_travel_info


router = APIRouter()
# why use a router?

@router.post("/location_info")
def get_location_info(data : LocationRequest):
    summary = generate_summary(
    city=data.name,
    user_prompt=data.preference
    )

    
    travel_info = get_travel_info(data.current_city, data.name)

    return {
        "location" : data.name,
        "summary" : summary,
        "distance" : travel_info["distance"],
        #"travel_time": travel_info["travel_time"],
        #"avg_cost" : travel_info["avg_cost"]
    }
