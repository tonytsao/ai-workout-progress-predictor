from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO

from app.services.workout_service import analyze_workout_dataframe

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/analyze")
async def analyze_workout(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        return analyze_workout_dataframe(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))