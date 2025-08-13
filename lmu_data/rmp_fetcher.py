from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RmpConfig:
    enabled: bool = False


def fetch_rmp(_cfg: RmpConfig) -> List[dict]:
    # Placeholder: RateMyProfessors content is subject to Terms of Service and technical protections.
    # Consider obtaining licensed datasets or manually exported snippets.
    # This function returns an empty list by default.
    return []