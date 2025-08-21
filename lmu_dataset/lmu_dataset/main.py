import os
from .seed import write_seed_jsonl

DEF_OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "lmu_seed.jsonl")

def main():
    write_seed_jsonl(DEF_OUT)
    print(f"Wrote seed JSONL to {DEF_OUT}")
