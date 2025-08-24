from datetime import date, datetime
from enum import Enum
from typing import Annotated, Any
from fastapi import FastAPI, Query, status
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware
from src import controllers
from src.db.database import create_db_engine


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HeathCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class PersonResponse(BaseModel):
    id: str


class Person(BaseModel):
    name: str
    cpf: str
    civil_state: str
    created_time: datetime = datetime.now()
    modified_time: datetime = datetime.now()
    birth_date: date


class PaginatedPersonsMeta(BaseModel):
    count: int
    criteria: dict[str, Any]
    page: int
    page_size: int


class PaginatedPersons(BaseModel):
    meta: PaginatedPersonsMeta
    data: list[Person]

    @classmethod
    def from_dict(
        cls, *, meta: dict[str, Any], data: list[dict[str, Any]]
    ) -> "PaginatedPersons":
        meta_ = PaginatedPersonsMeta(**meta)
        data_ = list(map(lambda record: Person(**record), data))
        return cls(meta=meta_, data=data_)


class OrderBy(str, Enum):
    created_time = "created_time"
    name = "name"
    civil_state = "civil_state"

    def __str__(self) -> str:
        return self.value


@app.get("/persons")
def list_persons(
    cpf: Annotated[str | None, Query(max_length=11)] = None,
    name: Annotated[str | None, Query()] = None,
    civil_state: Annotated[str | None, Query()] = None,
    page: Annotated[int | None, Query(ge=1)] = 1,
    page_size: Annotated[int | None, Query(le=10)] = 10,
    order_by: Annotated[OrderBy | None, Query()] = OrderBy.created_time,
    descending: Annotated[bool, Query()] = True,
    birth_date: Annotated[date | None, Query()] = None,
) -> PaginatedPersons:
    request = controllers.ListPersonsRequest(
        birth_date=birth_date,
        cpf=cpf,
        name=name,
        civil_state=civil_state,
        page=page,
        page_size=page_size,
        order_by=order_by,
        descending=descending,
    )
    engine = create_db_engine()
    with engine.connect() as connection:
        response = controllers.list_persons(request, connection)
    return PaginatedPersons.from_dict(
        meta={
            "count": response.count,
            "criteria": request.criteria,
            "page": page,
            "page_size": page_size,
        },
        data=response.data,
    )


@app.post("/person")
def upsert_person(person_model: Person) -> PersonResponse:
    engine = create_db_engine()
    with engine.connect() as connection:
        response = controllers.upsert_person(person_model, connection)
    return PersonResponse(id=response.id)


@app.get("/")
def index():
    return "Hello World!"


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Heath Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HeathCheck,
)
async def get_health() -> HeathCheck:
    """## Perform a Health Check

    Returns:
    --------
        HeathCheck: Returns a JSON response with the health status
    """
    return HeathCheck(status="OK")
