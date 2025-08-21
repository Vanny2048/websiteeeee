import json
from typing import Iterable, Dict

class JsonlWriter:
    def __init__(self, path: str):
        self.path = path

    def write_many(self, rows: Iterable[Dict]):
        with open(self.path, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

