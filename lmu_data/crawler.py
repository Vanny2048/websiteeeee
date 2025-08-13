from __future__ import annotations

import random
import time
from collections import deque
from dataclasses import dataclass
from typing import Iterable

import requests
from bs4 import BeautifulSoup
import trafilatura

from .utils import (
    setup_logger,
    is_allowed_by_robots,
    is_domain_allowed,
    should_skip_url,
    normalized_url,
    sleep_jitter,
)
from .text_clean import clean_text


@dataclass
class CrawlConfig:
    allowed_domains: list[str]
    disallow_file_types: list[str]
    max_pages: int
    request_timeout_s: int
    user_agent: str
    sleep_range_s: tuple[float, float]


@dataclass
class PageItem:
    url: str
    title: str
    text: str


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links: list[str] = []
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not href:
            continue
        if href.startswith("mailto:") or href.startswith("javascript:"):
            continue
        # Resolve relative URLs using BeautifulSoup's built-in handling via <base> would be ideal; 
        # fallback to requests compat by allowing normalization to handle.
        if href.startswith("/"):
            # prefix with scheme+host from base
            from urllib.parse import urlparse

            p = urlparse(base_url)
            href = f"{p.scheme}://{p.netloc}{href}"
        links.append(normalized_url(href))
    return links


def fetch_page(url: str, timeout_s: int, user_agent: str) -> tuple[str | None, str | None]:
    headers = {"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout_s)
        if resp.status_code != 200 or not resp.headers.get("content-type", "").startswith("text"):
            return None, None
        html = resp.text
        soup = BeautifulSoup(html, "lxml")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        return html, title
    except Exception:
        return None, None


def extract_main_text(html: str, url: str) -> str:
    try:
        extracted = trafilatura.extract(
            html,
            url=url,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
            no_fallback=False,
        )
        return clean_text(extracted or "")
    except Exception:
        return ""


def crawl(seeds: Iterable[str], cfg: CrawlConfig) -> list[PageItem]:
    logger = setup_logger()
    queue = deque(normalized_url(s) for s in seeds)
    seen_urls: set[str] = set()
    items: list[PageItem] = []

    while queue and len(items) < cfg.max_pages:
        url = queue.popleft()
        if url in seen_urls:
            continue
        seen_urls.add(url)

        if not is_domain_allowed(url, cfg.allowed_domains):
            continue
        if should_skip_url(url, cfg.disallow_file_types):
            continue
        if not is_allowed_by_robots(url, cfg.user_agent):
            continue

        html, title = fetch_page(url, cfg.request_timeout_s, cfg.user_agent)
        if not html:
            continue

        text = extract_main_text(html, url)
        if text and len(text) > 200:
            items.append(PageItem(url=url, title=title or url, text=text))

        # enqueue links
        links = extract_links(html, url)
        random.shuffle(links)
        for link in links:
            if link not in seen_urls and is_domain_allowed(link, cfg.allowed_domains):
                queue.append(link)

        sleep_jitter(cfg.sleep_range_s)

    logger.info(f"Crawled {len(items)} pages from {len(seeds)} seeds")
    return items