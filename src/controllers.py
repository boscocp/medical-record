from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Connection

from src.repositories import PersonRepository


@dataclass
class ListPersonsResponse:
    count: int
    data: list[dict[str, Any]]


@dataclass
class ListPersonsRequest:
    cpf: str
    name: str
    birth_date: str
    civil_state: str
    page: int
    page_size: int
    order_by: str
    descending: bool

    @property
    def criteria(self) -> dict[str, str | int | None]:
        return {
            "cpf": self.cpf,
            "name": self.name,
            "civil_state": self.civil_state,
            "birth_date": self.birth_date,
        }


def list_persons(
    request: ListPersonsRequest, connection: Connection
) -> ListPersonsResponse:
    repository = PersonRepository(connection)
    count = repository.count_by(request.criteria)
    data: Iterable[dict[str, Any]] = []
    if count > 0:
        data = repository.find_paginated(
            criteria=request.criteria,
            page=request.page,
            page_size=request.page_size,
            order_by=request.order_by,
            descending=request.descending,
        )
    return ListPersonsResponse(count, list(data))


@dataclass
class UpsertPersonResponse:
    id: str


def upsert_person(person_model, connection) -> UpsertPersonResponse:
    repository = PersonRepository(connection)

    if hasattr(person_model, "dict"):
        person_dict = person_model.dict()
    else:
        person_dict = dict(person_model)
    id = repository.upsert_person(person_dict)

    return UpsertPersonResponse(id=id)
