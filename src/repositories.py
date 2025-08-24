from collections.abc import Iterable
from typing import Any
from sqlalchemy import Connection, select, func
from src.models.medical_records_models import persons

PERSONS_LIST_COLUMNS = ", ".join(
    (
        "id",
        "cpf",
        "name",
        "birth_date",
        "civil_state",
        "created_time",
        "modified_time",
    )
)
UPDATE_COLUMNS = (
    "name",
    "cpf",
    "birth_date",
    "civil_state",
    "modified_time",
)


class RecordNotFoundError(RuntimeError):
    pass


class PersonRepository:
    def __init__(self, connection: Connection) -> None:
        """Database access layer"""
        self._connection = connection

    def find_by_id(self, id: str) -> dict[str, Any]:
        stmt = select(persons).where(persons.c.id == id)
        result = self._connection.execute(stmt)
        record = result.fetchone()

        if record is None:
            raise RecordNotFoundError(f"Peron '{id}' not found")
        return record._asdict()

    def count_by(self, criteria: dict[str, str | int | None]) -> int:
        conditions = [
            getattr(persons.c, key) == value
            for key, value in criteria.items()
            if value is not None
        ]
        stmt = select(func.count()).select_from(persons)
        if conditions:
            stmt = stmt.where(*conditions)

        result = self._connection.execute(stmt)
        (count,) = result.fetchone()
        return int(count)

    def find_paginated(
        self,
        criteria: dict[str, str | int | None],
        page: int,
        page_size: int,
        order_by: str,
        descending: bool,
    ) -> Iterable[dict[str, Any]]:
        conditions = self._build_conditions_str(criteria)
        offset = page_size * (page - 1)
        order_column = getattr(persons.c, order_by)
        order_clause = order_column.desc() if descending else order_column.asc()

        stmt = (
            select(persons)
            .where(*conditions)
            .order_by(order_clause)
            .limit(page_size)
            .offset(offset)
        )

        for record in self._connection.execute(stmt):
            yield record._asdict()

    def _build_conditions_str(self, criteria: dict[str, str | int | None]) -> str:
        conditions = [
            getattr(persons.c, key) == value
            for key, value in criteria.items()
            if value is not None
        ]
        return conditions
