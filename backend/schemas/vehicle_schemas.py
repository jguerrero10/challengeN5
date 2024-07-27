from pydantic import BaseModel, Field


class Vehicle(BaseModel):
    patent_plate: str = Field(..., title="Patent Plate Name", description="Patent Plate Name of the Vehicle")
    brand: str = Field(..., title="Brand Name", description="Brand Name of Vehicle")
    color: str = Field(..., title="Color Name", description="Color's vehicle")

    model_config = {
        "json_schema_extra": {
            "example": {
                "patent_plate": "KXR243",
                "brand": "Sandero",
                "color": "Blue",
            }
        }
    }
