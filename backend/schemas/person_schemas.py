from typing import Annotated, Optional, List

from pydantic import BaseModel, BeforeValidator, EmailStr, Field

from schemas.vehicle_schemas import Vehicle

PyObjectId = Annotated[str, BeforeValidator(str)]


class Person(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id", serialization_alias="id")
    name: str = Field(..., title="Name", description="Person's name")
    email: EmailStr = Field(..., title="Email", description="Person's email")
    vehicles: Optional[List[Vehicle]] = Field([], title="Vehicles", description="Person's vehicles")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "23hsd6gas",
                "name": "John Poe",
                "email": "john.poe@email.com",
                "vehicles": [
                    {
                        "patent_plate": "KXR243",
                        "brand": "Sandero",
                        "color": "Blue",
                    }
                ]
            }
        }
    }


class PersonCreate(BaseModel):
    name: str = Field(..., title="Name", description="Person's name")
    email: EmailStr = Field(..., title="Email", description="Person's email")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Poe",
                "email": "john.poe@email.com",
            }
        }
    }


class PersonUpdate(BaseModel):
    name: str = Field(..., title="Name", description="Person's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Poe"
            }
        }
    }