from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path

import yaml

from lmu_data.crawler import crawl, CrawlConfig, PageItem
from lmu_data.reddit_fetcher import fetch_reddit, RedditConfig
from lmu_data.rmp_fetcher import fetch_rmp, RmpConfig
from lmu_data.qa_generator import build_dataset, QAGeneratorConfig
from lmu_data.utils import setup_logger


def load_config(path: str | None) -> dict:
    if not path:
        path = "config.yml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="LMU Q/A dataset pipeline")
    parser.add_argument("--out", required=True, help="Output JSONL path")
    parser.add_argument("--config", default="config.yml")
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--max-total", type=int, default=2000)
    parser.add_argument("--no-reddit", action="store_true")
    parser.add_argument("--enable-rmp", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.config)

    logger = setup_logger()

    seeds = cfg.get("seeds", [])
    allowed_domains = cfg.get("allowed_domains", [])
    crawl_cfg = cfg.get("crawl", {})
    reddit_cfg = cfg.get("reddit", {})
    rmp_cfg = cfg.get("rmp", {})
    qa_cfg = cfg.get("qa_generation", {})

    random.seed(qa_cfg.get("seed", 17))

    crawl_conf = CrawlConfig(
        allowed_domains=allowed_domains,
        disallow_file_types=crawl_cfg.get("disallow_file_types", []),
        max_pages=args.max_pages or crawl_cfg.get("max_pages", 200),
        request_timeout_s=crawl_cfg.get("request_timeout_s", 15),
        user_agent=crawl_cfg.get("user_agent", "lmudata-bot/0.1"),
        sleep_range_s=tuple(crawl_cfg.get("sleep_range_s", [0.2, 1.0])),
    )

    qa_conf = QAGeneratorConfig(
        max_pairs_per_page=qa_cfg.get("max_pairs_per_page", 20),
        max_pairs_from_reddit_post=qa_cfg.get("max_pairs_from_reddit_post", 5),
        voice=qa_cfg.get("voice", "casual"),
        seed=qa_cfg.get("seed", 17),
    )

    logger.info("Starting crawl…")
    pages: list[PageItem] = crawl(seeds, crawl_conf)

    items: list[dict] = [
        {"source": "web", "url": p.url, "title": p.title, "text": p.text}
        for p in pages
    ]

    if not args.no_reddit and reddit_cfg.get("enabled", True):
        logger.info("Fetching Reddit posts…")
        red = fetch_reddit(
            RedditConfig(
                subreddits=reddit_cfg.get("subreddits", []),
                max_posts_per_sub=reddit_cfg.get("max_posts_per_sub", 100),
                fetch_comments=reddit_cfg.get("fetch_comments", True),
                max_comments_per_post=reddit_cfg.get("max_comments_per_post", 50),
            )
        )
        items.extend(red)

    if args.enable_rmp and rmp_cfg.get("enabled", False):
        logger.info("Fetching RateMyProfessors…")
        items.extend(fetch_rmp(RmpConfig(enabled=True)))

    logger.info(f"Generating Q/A from {len(items)} items…")
    dataset = build_dataset(items, qa_conf, max_total=args.max_total)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in dataset:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    logger.info(f"Wrote {len(dataset)} examples to {out_path}")


if __name__ == "__main__":
    main()