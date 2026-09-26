import base64
import json
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from energyos.domain.errors import InvalidCursor
from energyos.domain.pagination import decode_cursor, encode_cursor


def test_cursor_round_trip() -> None:
    created_at = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    entity_id = uuid4()
    assert decode_cursor(encode_cursor(created_at, entity_id)) == (created_at, entity_id)


def test_cursor_rejects_a_naive_timestamp() -> None:
    with pytest.raises(ValueError):
        encode_cursor(datetime(2026, 1, 1), uuid4())

    payload = base64.urlsafe_b64encode(
        json.dumps({"created_at": "2026-01-01T00:00:00", "id": str(uuid4())}).encode()
    ).decode()
    with pytest.raises(InvalidCursor):
        decode_cursor(payload)


def test_cursor_rejects_garbage() -> None:
    with pytest.raises(InvalidCursor):
        decode_cursor("not-a-cursor")
