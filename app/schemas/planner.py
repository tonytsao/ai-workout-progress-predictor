from typing import Optional, Dict
from pydantic import BaseModel, Field


class PlannerRequest(BaseModel):
    goal: str = Field(..., description="strength, hypertrophy, or general_fitness")
    days_per_week: int = Field(..., ge=2, le=6)
    experience: str = Field(..., description="beginner, intermediate, or advanced")
    plateau_summary: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional plateau risk summary, e.g. {'bench_press': 'High'}"
    )