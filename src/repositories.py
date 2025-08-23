from collections.abc import Iterable
from datetime import datetime
from typing import Any
from sqlalchemy import Connection, select, text, func
from sqlalchemy.dialects.mysql import insert
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
    "civil_state"
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
        str_where = self._build_conditions_str(criteria)
        stmt = select(func.count()).select_from(persons).where(text(str_where))
        result = self._connection.execute(stmt, criteria)
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
        str_where = self._build_conditions_str(criteria)
        offset = page_size * (page - 1)
        order_by_stmt = f"{order_by} {'DESC' if descending else 'ASC'}"
        stmt = (
            select(text(PERSONS_LIST_COLUMNS))
            .select_from(persons)
            .where(text(str_where))
            .limit(page_size)
            .offset(offset)
            .order_by(text((order_by_stmt)))
        )
        for record in self._connection.execute(stmt, criteria):
            yield record._asdict()

    def _build_conditions_str(self, criteria: dict[str, str | int | None]) -> str:
        conditions = []
        for key, value in criteria.items():
            if value is None:
                continue
            conditions.append(f"{key} =: {key}")
        return " AND ".join(conditions)

    def upsert_person(self, person_model):
        insert_stmt = insert(persons).values(**person_model)
        update_model = {}
        for key in UPDATE_COLUMNS:
            update_model[key] = person_model[key]

        upsert_stmt = insert_stmt.on_duplicate_key_update(**update_model)

        result = self._connection.execute(upsert_stmt)
        # self._connection.commit()
        return result  # Retorna o modelo inserido
