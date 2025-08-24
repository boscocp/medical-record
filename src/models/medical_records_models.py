from datetime import datetime
import re
import uuid
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    String,
    Date,
    MetaData,
    Enum,
    Text,
    UniqueConstraint,
    TIMESTAMP,
)
from sqlalchemy.dialects.mysql import insert

metadata = MetaData()

UPDATE_COLUMNS = ("name", "cpf", "birth_date", "civil_state")
# Enum ou lista de opções para estado civil
MARITAL_STATUS_CHOICES = ("S", "M", "D")  # Single, Married, Divorced
CPF_REGEX = re.compile(
    r"^([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})$"
)

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
# TODO implement these 2 tables
# 1:N
appointments = Table(
    "appointment",
    metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("person_id", String(36), ForeignKey("person.id"), nullable=False),
    Column("appointment_date", TIMESTAMP(), nullable=False),
    Column("description", String(500), nullable=True),
    Column("created_time", TIMESTAMP(), nullable=False),
    Column("modified_time", TIMESTAMP(), nullable=False),
)
# 1:1
patient_records = Table(
    "patient_record",
    metadata,
    Column("id", String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
    Column(
        "person_id", String(36), ForeignKey("person.id"), unique=True, nullable=False
    ),
    Column("medical_history", Text, nullable=True),
    Column("allergies", Text, nullable=True),
    Column("created_time", TIMESTAMP(), nullable=False),
    Column("modified_time", TIMESTAMP(), nullable=False),
)


def _validate_person_data(data):
    if not CPF_REGEX.match(data["cpf"]):
        raise ValueError("CPF must be valid")
    if data["civil_state"] not in MARITAL_STATUS_CHOICES:
        raise ValueError("Invalid marital status")
    return data


def upsert_person(connection, person_model) -> str:
    _validate_person_data(person_model)
    now = datetime.now()

    if not person_model.get("created_time"):
        person_model["created_time"] = now
    person_model["modified_time"] = now

    insert_stmt = insert(persons).values(**person_model)
    update_model = {}
    for key in UPDATE_COLUMNS:
        update_model[key] = person_model[key]

    upsert_stmt = insert_stmt.on_duplicate_key_update(**update_model)

    result = connection.execute(upsert_stmt)
    connection.commit()
    return result.inserted_primary_key[0]
