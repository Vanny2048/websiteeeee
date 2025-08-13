from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Iterable

import requests

from .text_clean import clean_text


@dataclass
class RedditConfig:
    subreddits: list[str]
    max_posts_per_sub: int = 100
    fetch_comments: bool = True
    max_comments_per_post: int = 50


UA = "Mozilla/5.0 (X11; Linux x86_64) lmudata-bot/0.1"


def _get_json(url: str):
    headers = {"User-Agent": UA}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        return None
    return resp.json()


def fetch_reddit(cfg: RedditConfig) -> list[dict]:
    results: list[dict] = []
    for sub in cfg.subreddits:
        after = None
        fetched = 0
        while fetched < cfg.max_posts_per_sub:
            limit = min(100, cfg.max_posts_per_sub - fetched)
            url = f"https://www.reddit.com/r/{sub}/.json?limit={limit}"
            if after:
                url += f"&after={after}"
            data = _get_json(url)
            if not data:
                break
            children = data.get("data", {}).get("children", [])
            if not children:
                break
            for ch in children:
                post = ch.get("data", {})
                post_id = post.get("id")
                permalink = post.get("permalink")
                title = post.get("title") or ""
                selftext = post.get("selftext") or ""
                url_full = f"https://www.reddit.com{permalink}" if permalink else ""
                text = clean_text(f"{title}\n\n{selftext}")
                if text:
                    results.append({
                        "source": "reddit",
                        "url": url_full,
                        "title": title,
                        "text": text,
                    })
                if cfg.fetch_comments and post_id and permalink:
                    comments_url = f"https://www.reddit.com{permalink}.json?limit={cfg.max_comments_per_post}"
                    thread = _get_json(comments_url)
                    if isinstance(thread, list) and len(thread) > 1:
                        comments = thread[1].get("data", {}).get("children", [])
                        for c in comments[: cfg.max_comments_per_post]:
                            body = c.get("data", {}).get("body")
                            if body:
                                results.append({
                                    "source": "reddit_comment",
                                    "url": url_full,
                                    "title": title,
                                    "text": clean_text(body),
                                })
                fetched += 1
            after = data.get("data", {}).get("after")
            if not after:
                break
            time.sleep(1.0)
    return results