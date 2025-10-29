from fastapi import APIRouter
from app.ml.predict import predict_bike

router = APIRouter(prefix="/bikes", tags=["Bikes"])

@router.get("/score/{bike_id}")
def score_bike(bike_id: int):
    probs = predict_bike(bike_id)
    return {"bike_id": bike_id, "probabilities": probs}
