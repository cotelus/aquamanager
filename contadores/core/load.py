import os
from typing import Any

def get_venv(name: str) -> Any:
    value = None

    if name in os.environ:
        value = os.environ.get(name)

    return value
