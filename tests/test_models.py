import pytest
from unittest.mock import Mock, patch
from datetime import date, datetime
from src.models.medical_records_models import upsert_person, persons


@patch("src.models.medical_records_models.insert")
def test_upsert_person_executes_insert(mock_insert: Mock):
    # Arrange
    model = {
        "name": "Any first",
        "cpf": "12345678901",
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

    # Act
    upsert_person(connection, model)

    # Assert
    mock_insert.assert_called_once_with(persons)
    mock_insert_clause.values.assert_called_once_with(**model)
    mock_insert_clause.on_duplicate_key_update.assert_called_once()
    connection.execute.assert_called_once_with(mock_insert_clause)
