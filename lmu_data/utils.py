import re
import time
import random
import logging
from urllib.parse import urlparse
from urllib import robotparser
from functools import lru_cache
from url_normalize import url_normalize


def setup_logger(level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("lmu_data")


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower()


@lru_cache(maxsize=256)
def get_robot_parser(base_url: str) -> robotparser.RobotFileParser:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        pass
    return rp


def is_allowed_by_robots(url: str, user_agent: str = "*") -> bool:
    domain = get_domain(url)
    scheme = urlparse(url).scheme or "https"
    base_url = f"{scheme}://{domain}"
    rp = get_robot_parser(base_url)
    try:
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True


def normalized_url(url: str) -> str:
    try:
        return url_normalize(url)
    except Exception:
        return url


def should_skip_url(url: str, disallow_exts: list[str]) -> bool:
    lowered = url.lower().split("?")[0].split("#")[0]
    return any(lowered.endswith(ext) for ext in disallow_exts)


def sleep_jitter(range_s: tuple[float, float]) -> None:
    low, high = range_s
    time.sleep(random.uniform(low, high))


def is_domain_allowed(url: str, allowed_domains: list[str]) -> bool:
    domain = get_domain(url)
    return any(domain == d or domain.endswith("." + d) for d in allowed_domains)


_slug_re = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_len: int = 64) -> str:
    s = text.lower()
    s = _slug_re.sub("-", s).strip("-")
    return s[:max_len]