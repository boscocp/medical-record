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
            "civil_state": self.civil_state,
            "birth_date": self.birth_date,
        }


def list_persons(request: ListPersonsRequest, connection: Connection) -> ListPersonsResponse:
    repository = PersonRepository(connection)
    count = repository.count_by(request.criteria)
    data: Iterable[dict[str, Any]] = []
    if count > 0:
        data = repository.find_paginated(
            request.criteria,
            request.page,
            request.page_size,
            request.order_by,
            request.descending,
        )
    return ListPersonsResponse(count, list(data))

# ...existing code...


@dataclass
class UpsertPersonResponse:
    id: str
    name: str


def upsert_person(person_model, connection) -> UpsertPersonResponse:
    repository = PersonRepository(connection)
    # Converte o modelo Pydantic para dict, se necessário
    if hasattr(person_model, "dict"):
        person_dict = person_model.dict()
    else:
        person_dict = dict(person_model)
    repository.upsert_person(person_dict)
    # Após o upsert, busca o registro atualizado/inserido
    person = repository.find_by_id(person_dict["id"])
    return UpsertPersonResponse(id=person["id"], name=person["name"])
