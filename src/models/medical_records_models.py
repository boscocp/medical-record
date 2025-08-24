from typing import Any
import uuid
import re
from sqlalchemy import (
    Table,
    Column,
    String,
    Date,
    MetaData,
    Enum,
    UniqueConstraint,
    TIMESTAMP,
    Connection,
)
from sqlalchemy.dialects.mysql import insert

metadata = MetaData()

UPDATE_COLUMNS = ("name", "cpf", "birth_date", "civil_state")
# Enum ou lista de opções para estado civil
MARITAL_STATUS_CHOICES = ("S", "M", "D")  # Single, Married, Divorced

CPF_REGEX = re.compile(
    r"^([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})$"
)


def _validate_person_data(data):
    if not CPF_REGEX.match(data["cpf"]):
        raise ValueError("CPF must be valid")
    if data["civil_state"] not in MARITAL_STATUS_CHOICES:
        raise ValueError("Invalid marital status")
    return data


persons = Table(
    "person",
    metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("name", String(200), nullable=False),
    Column("cpf", String(14), nullable=False, unique=True),
    Column("birth_date", Date, nullable=False),
    Column(
        "civil_state",
        Enum(*MARITAL_STATUS_CHOICES, name="marital_status"),
        nullable=False,
        default="S",
    ),
    Column("created_time", TIMESTAMP(), nullable=False),
    Column("modified_time", TIMESTAMP(), nullable=False),
    UniqueConstraint("cpf", name="uq_person_cpf"),
)


def upsert_person(connection: Connection, model: dict[str, Any]) -> None:
    insert_stmt = insert(persons).values(**model)
    update_model = {}
    for key in UPDATE_COLUMNS:
        update_model[key] = model[key]

    upsert_stmt = insert_stmt.on_duplicate_key_update(**update_model)

    connection.execute(upsert_stmt)
