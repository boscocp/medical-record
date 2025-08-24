from unittest.mock import Mock, patch
from datetime import date, datetime

import pytest
from src.models.medical_records_models import upsert_person, persons


@patch("src.models.medical_records_models.insert")
def test_upsert_person_executes_insert(mock_insert: Mock):
    # Arrange
    model = {
        "name": "Any first",
        "cpf": "97348458025",
        "birth_date": date(1990, 1, 1),
        "civil_state": "S",
        "created_time": datetime.now(),
        "modified_time": datetime.now(),
    }

    connection = Mock()

    # Mocks
    mock_insert_clause = Mock()
    mock_insert_clause.values.return_value = mock_insert_clause
    mock_insert_clause.on_duplicate_key_update.return_value = mock_insert_clause
    mock_insert.return_value = mock_insert_clause

    mock_result = Mock()
    mock_result.inserted_primary_key = ["mocked-id"]
    connection.execute.return_value = mock_result
    # Act
    returned_id = upsert_person(connection, model)

    # Assert
    assert returned_id == "mocked-id"
    connection.execute.assert_called_once_with(mock_insert_clause)
    connection.commit.assert_called_once()
    mock_insert.assert_called_once_with(persons)
    mock_insert_clause.values.assert_called_once_with(**model)
    mock_insert_clause.on_duplicate_key_update.assert_called_once()
    connection.execute.assert_called_once_with(mock_insert_clause)


@patch("src.models.medical_records_models.insert")
def test_upsert_person_invalid_cpf(mock_insert: Mock):
    # Arrange
    model = {
        "name": "Any first",
        "cpf": "x",
        "birth_date": date(1990, 1, 1),
        "civil_state": "S",
        "created_time": datetime.now(),
        "modified_time": datetime.now(),
    }

    connection = Mock()

    # Mocks
    mock_insert_clause = Mock()
    mock_insert_clause.values.return_value = mock_insert_clause
    mock_insert_clause.on_duplicate_key_update.return_value = mock_insert_clause
    mock_insert.return_value = mock_insert_clause

    mock_result = Mock()
    mock_result.inserted_primary_key = ["mocked-id"]
    connection.execute.return_value = mock_result
    # Act & Assert
    with pytest.raises(ValueError, match="CPF must be valid"):
        upsert_person(connection, model)
