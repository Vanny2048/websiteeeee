import json, os

SEED_ENTRIES = [
    {"instruction": "Where can I find info on campus safety services?", "output": "Visit LMU Department of Public Safety for emergency procedures, escorts, and contacts."},
    {"instruction": "How do I see dining hall hours?", "output": "Check LMU Dining/CampusDish site for current hours and locations."},
]

def write_seed_jsonl(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for row in SEED_ENTRIES:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
