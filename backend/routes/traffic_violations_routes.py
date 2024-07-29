from typing import List

from fastapi import APIRouter, Query, Depends, HTTPException, status
from pydantic import EmailStr

from database.crud import search_objects, add_object, update_object
from schemas.officer_schemas import Officer
from schemas.person_schemas import Person, PersonCreate
from schemas.traffic_violations_schemas import TrafficViolations
from schemas.user_schemas import TokenData
from utils.auth_utils import define_role
from utils.enums import Role
from utils.token_manage import get_current_user

traffic_violations_router = APIRouter()


@traffic_violations_router.get("/", response_model=List[TrafficViolations])
async def get_violations_by_person(
        person_email: EmailStr = Query(
            ...,
            example="example@mail.com",
            title="Person Email", description="Person Email"
        ),
        token_data: TokenData = Depends(get_current_user)
):
    define_role(token_data, Role.OFFICER)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = person_search[0]


@traffic_violations_router.post("/", response_model=TrafficViolations)
async def create_traffic_violation(
        traffic_violations: TrafficViolations,
        person: PersonCreate,
        token_data: TokenData = Depends(get_current_user)
):
    define_role(token_data, Role.OFFICER)
    officer_search = await search_objects("officers", "username", token_data.username)
    if not officer_search:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Officer not found")
    officer = Officer(**officer_search[0])
    traffic_violations.officer = officer
    person_search = await search_objects("persons", "email", person.email)
    if person_search:
        person = Person(**person_search[0])
    else:
        person_added = await add_object("persons", dict(person))
        person = Person(**person_added)
    traffic_violations_list = person.traffic_violations
    traffic_violations_list.append(traffic_violations)
    traffic_violations_dict = [
        {
            "patent_plate": traffic_violations.patent_plate,
            "timestamp": traffic_violations.timestamp,
            "comments": traffic_violations.comments,
            "officer": dict(traffic_violation.officer)
        }
        for traffic_violation in traffic_violations_list
    ]
    person_dict = dict(person)
    person_dict["traffic_violations"] = traffic_violations_dict
    person_dict["vehicles"] = [dict(vehicle) for vehicle in person.vehicles] if person.vehicles is not None else []
    await update_object("persons", person.id, person_dict)
    return traffic_violations
