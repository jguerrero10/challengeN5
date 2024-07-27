from pydantic import BaseModel, Field


class Officer(BaseModel):
    name: str = Field(..., title="Name", description="Name of the officer")
    number_identifier: str = Field(..., title="Number Identifier", description="Identifier for the officer")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Raphy Dion",
                "number_identifier": "12345",
            }
        }
    }
