# LMU Data Scraper and Q/A Generator

## Quickstart

1. Create venv and install deps
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure sources in `config.yml` (defaults target LMU domains + Reddit).

3. Run crawl + generate
```
python scripts/run_pipeline.py --out data/lmu_train.jsonl --max-pages 300
```

4. Inspect sample
```
head -n 5 data/lmu_train.jsonl | sed -n '1,5p'
```

## Output
- JSONL lines with {"instruction", "output"} in a casual student voice.

## Notes
- Respects robots.txt. For Reddit, unauthenticated read via PRAW may be rate-limited.
- You can expand `max-pages` and tweak stylistic prompts in `config.yml`.