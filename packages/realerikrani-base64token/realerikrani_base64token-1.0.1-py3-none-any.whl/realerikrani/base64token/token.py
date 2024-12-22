import base64
import binascii
import json
from typing import Any


def encode(data: list[tuple[str, Any]] | None) -> str | None:
    if data is None:
        return None
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()


def decode(token: str) -> dict | None:
    try:
        return dict(json.loads(base64.urlsafe_b64decode(token).decode()))
    except (json.JSONDecodeError, binascii.Error):
        return None
