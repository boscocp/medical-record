import pytest
import uuid
from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.medical_records_models import metadata, persons, upsert_person


@pytest.fixture(scope="function")
def connection():
    # Use um banco em memória para testes
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    conn = engine.connect()
    yield conn
    conn.close()


def test_create_person(connection):
    model = {
        "name": "Teste Criacao",
        "cpf": "12345678901",
        "birth_date": date(1990, 1, 1),
        "civil_state": "S",
        "created_time": datetime.now(),
        "modified_time": datetime.now(),
    }
    upsert_person(connection, model)
    result = connection.execute(persons.select().where(
        persons.c.cpf == "12345678901")).fetchone()
    assert result is not None
    assert result["name"] == "Teste Criacao"
    assert result["cpf"] == "12345678901"


def test_update_person(connection):
    # Primeiro cria
    model = {
        "name": "Teste Update",
        "cpf": "12345678902",
        "birth_date": date(1991, 2, 2),
        "civil_state": "M",
        "created_time": datetime.now(),
        "modified_time": datetime.now(),
    }
    upsert_person(connection, model)
    # Atualiza
    model_update = model.copy()
    model_update["name"] = "Nome Atualizado"
    upsert_person(connection, model_update)
    result = connection.execute(persons.select().where(
        persons.c.cpf == "12345678902")).fetchone()
    assert result is not None
    assert result["name"] == "Nome Atualizado"
