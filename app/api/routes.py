from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import StringIO

from app.schemas.response import ApiResponse
from app.schemas.planner import PlannerRequest
from app.services.workout_service import analyze_workout_dataframe
from app.services.planner_service import create_workout_plan

router = APIRouter()

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


@router.get("/health", response_model=ApiResponse)
def health_check():
    return ApiResponse(
        success=True,
        message="Service is healthy.",
        data={"status": "ok"},
    )


@router.post("/analyze", response_model=ApiResponse)
async def analyze_workout(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 2 MB limit.")

    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        result = analyze_workout_dataframe(df)

        return ApiResponse(
            success=True,
            message="Workout analysis completed successfully.",
            data=result,
        )

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded CSV.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="Uploaded CSV file is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="CSV format is invalid.")


@router.post("/planner", response_model=ApiResponse)
def planner(request: PlannerRequest):
    result = create_workout_plan(
        goal=request.goal,
        days_per_week=request.days_per_week,
        experience=request.experience,
        plateau_summary=request.plateau_summary,
    )

    return ApiResponse(
        success=True,
        message="Workout plan generated successfully.",
        data=result,
    )

