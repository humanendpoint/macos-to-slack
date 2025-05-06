# tests/test_main.py

import pytest
from unittest.mock import patch
from bin import main


# Test JSON retrieval function with a mock response
@patch("bin.main.requests.get")
def test_retrieve_json_data_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    result = main.retrieve_json_data()
    assert result == {"key": "value"}


# Test if None is returned when status code is not 200
@patch("bin.main.requests.get")
def test_retrieve_json_data_failure(mock_get):
    mock_get.return_value.status_code = 500
    result = main.retrieve_json_data()
    assert result is None
