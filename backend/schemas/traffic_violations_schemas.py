from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from schemas.officer_schemas import Officer


class TrafficViolations(BaseModel):
    patent_plate: str = Field(..., title="Patent Plate Name", description="Patent Plate Name of the Vehicle")
    timestamp: datetime = Field(..., title="Timestamp", description="Timestamp of the traffic violation")
    comments: str = Field(..., title="Comments", description="Comment of the traffic violation")
    officer: Optional[Officer] = Field(None, title="Officer", description="Officer of the traffic violation")

    model_config = {
        "json_schema_extra": {
            "example": {
                "patent_plate": "KXR243",
                "timestamp": datetime.now(),
                "comments": "Lorem ipsum dolor sit amet..",
            }
        }
    }
