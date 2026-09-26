import base64
import json
from datetime import datetime
from uuid import UUID

from energyos.domain.errors import InvalidCursor


def encode_cursor(created_at: datetime, entity_id: UUID) -> str:
    if created_at.tzinfo is None:
        raise ValueError("cursor timestamps must include a timezone")
    payload = json.dumps(
        {"created_at": created_at.isoformat(), "id": str(entity_id)},
        separators=(",", ":"),
    ).encode()
    return base64.urlsafe_b64encode(payload).decode()


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    padded = cursor + "=" * (-len(cursor) % 4)
    try:
        raw = base64.urlsafe_b64decode(padded.encode())
        payload = json.loads(raw)
        if not isinstance(payload, dict):
            raise InvalidCursor
        created_raw = payload.get("created_at")
        id_raw = payload.get("id")
        if not isinstance(created_raw, str) or not isinstance(id_raw, str):
            raise InvalidCursor
        created_at = datetime.fromisoformat(created_raw)
        entity_id = UUID(id_raw)
    except (ValueError, json.JSONDecodeError, TypeError) as exc:
        raise InvalidCursor from exc
    if created_at.tzinfo is None:
        raise InvalidCursor
    return created_at, entity_id
