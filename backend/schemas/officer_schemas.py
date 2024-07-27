from typing import Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]


class Officer(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id", serialization_alias="id")
    name: str = Field(..., title="Name", description="Name of the officer")
    number_identifier: str = Field(..., title="Number Identifier", description="Identifier for the officer")
    username: str = Field(..., title="Username", description="Username for the officer")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Raphy Dion",
                "number_identifier": "12345",
            }
        }
    }


class OfficerCreate(BaseModel):
    name: str = Field(..., title="Name", description="Name of the officer")
    number_identifier: str = Field(..., title="Number Identifier", description="Identifier for the officer")
    username: str = Field(..., title="Username", description="Username for the officer")
    password: str = Field(..., title="Password", description="Password for the officer")


class OfficerUpdate(BaseModel):
    name: Optional[str] = Field(..., title="Name", description="Name of the officer")
