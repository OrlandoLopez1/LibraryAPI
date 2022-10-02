import pytest
from main import *

test_id = 9999


def test_adds_book_to_library_properly():
    data = {"name": "test", "type": "test", "author": "test test", "page_count": 1, "genre": "test",
            "progress": "test"}
    desired_result = {"id": test_id, "name": "test", "type": "test", "author": "test test", "page_count": 1,
                      "genre": "test", "progress": "test"}
    result = create(str(test_id), data)
    assert desired_result == result.json()


def test_adding_exisiting_book_returns_409():
    data = {"name": "test", "type": "test", "author": "test test", "page_count": 1, "genre": "test",
            "progress": "test"}
    result = create(str(test_id), data)
    assert result.status_code == 409


def test_reads_book_info_properly():
    result = read(str(test_id))
    assert result.status_code == 200


def test_updates_book_info_properly():
    data = {"name": "tested", "type": "tested", "author": "tested tested", "page_count": 1, "genre": "tested",
            "progress": "tested"}
    desired_result = {"id": test_id, "name": "tested", "type": "tested", "author": "tested tested", "page_count": 1,
                      "genre": "tested", "progress": "tested"}
    result = update(str(test_id), data)
    assert desired_result == result.json()


def test_update_failing_returns_404():
    result = update(str(test_id), {"name": "test"})
    assert result.status_code == 400


def test_deletes_book_properly():
    result = delete_(str(test_id))
    assert result.status_code == 200


def test_deleting_nonexisting_book_returns_404():
    result = delete_(str(test_id))
    assert result.status_code == 404


def test_reading_nonexisting_book_return_404():
    result = read(str(test_id))
    assert result.status_code == 404
