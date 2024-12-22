from dataclasses import asdict, dataclass, field
import datetime
import json
from pathlib import Path
import random
from typing import Sequence
import uuid


@dataclass
class Choice:
    name: str
    trials: int = 0
    successes: int = 0
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @property
    def json(self) -> dict:
        data = asdict(self)
        data["id"] = str(data["id"])
        return data
