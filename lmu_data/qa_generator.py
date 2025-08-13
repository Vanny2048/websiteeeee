from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Iterable

from rapidfuzz import fuzz

from .text_clean import clean_text, split_sentences


CASUAL_PREFIXES = [
    "tbh",
    "ngl",
    "low-key",
    "imo",
    "fr fr",
]

CASUAL_PHRASES = [
    "no cap",
    "for real",
    "kinda depends",
    "vibes",
    "heads up",
    "pro tip",
    "check the site to be safe",
]


@dataclass
class QAGeneratorConfig:
    max_pairs_per_page: int = 20
    max_pairs_from_reddit_post: int = 5
    voice: str = "casual"
    seed: int = 17


def _voiceify(answer: str) -> str:
    a = answer.strip()
    if not a:
        return a
    add_prefix = random.random() < 0.35
    if add_prefix:
        a = f"{random.choice(CASUAL_PREFIXES)}, {a}"
    if random.random() < 0.25:
        a = a + ", " + random.choice(CASUAL_PHRASES)
    return a


TOPIC_TEMPLATES = [
    {
        "topic": "housing",
        "patterns": [r"housing|residence|dorm|room|move[- ]?in|ra|microwave|hot plate"],
        "instructions": [
            "what's the deal with dorm rules?",
            "when's move-in and what can't I bring?",
            "are microwaves allowed in rooms?",
        ],
        "answers": [
            "dorms have the usual rules—no hot plates or open flames, microwaves are usually a no-go in rooms",
            "move-in dates drop via email; bring the basics and skip anything with heating elements",
            "check your housing portal for specifics on your hall; each building has its quirks",
        ],
    },
    {
        "topic": "parking",
        "patterns": [r"parking|permit|garage|lot|shuttle|scooter|bike"],
        "instructions": [
            "is parking worth it?",
            "how do permits work?",
            "can I bring a scooter?",
        ],
        "answers": [
            "permits let you enter lots but spots aren't guaranteed",
            "if you can swing it, scooters/bikes are clutch for quick hops",
            "check the parking portal for permit types and blackout dates",
        ],
    },
    {
        "topic": "dining",
        "patterns": [r"dining|meal plan|caf(e|\u00e9)|food|vegan|vegetarian|allergen"],
        "instructions": [
            "is the meal plan worth it?",
            "what are dining hours like?",
            "any good vegan options?",
        ],
        "answers": [
            "meal plans are convenient if you're on campus a lot; hours vary by spot",
            "there are usually vegetarian and vegan options; menus rotate",
            "grab hours/menus from the dining page before you head out",
        ],
    },
    {
        "topic": "academics",
        "patterns": [r"major|minor|advisor|advising|registration|add/drop|prereq|syllabus"],
        "instructions": [
            "can I switch majors easily?",
            "how does add/drop work?",
            "where do I find prerequisites?",
        ],
        "answers": [
            "switching is doable but some programs are capped—check with advising",
            "add/drop windows open each term in the portal; watch deadlines",
            "catalog lists prereqs; your advisor can clear roadblocks",
        ],
    },
    {
        "topic": "library",
        "patterns": [r"library|study room|printer|printing|loan|checkout|hours"],
        "instructions": [
            "are study rooms bookable?",
            "what are library hours?",
            "how do I print on campus?",
        ],
        "answers": [
            "study rooms are bookable online; show up or you lose the slot",
            "hours shift during finals—check the calendar",
            "load funds and print from campus printers; follow the IT guide",
        ],
    },
    {
        "topic": "athletics",
        "patterns": [r"basketball|lions|game|ticket|intramural|rec|gym|burns"],
        "instructions": [
            "is gym access free?",
            "how do I join intramurals?",
            "where do I get game tickets?",
        ],
        "answers": [
            "gym access is included once you complete the waiver",
            "intramurals open sign-ups each term—spaces fill fast",
            "tickets info is on athletics—students often get deals",
        ],
    },
    {
        "topic": "mail",
        "patterns": [r"mail|package|amazon|delivery|campus mail"],
        "instructions": [
            "where do I pick up packages?",
            "can someone else grab my mail?",
        ],
        "answers": [
            "you'll get an email when it's ready; pickup at the campus mail center",
            "bring your ID; mail staff won't release to others without authorization",
        ],
    },
    {
        "topic": "safety",
        "patterns": [r"security|dps|police|escort|emergency|alert"],
        "instructions": [
            "is campus safe at night?",
            "does LMU have escorts?",
        ],
        "answers": [
            "security patrols are around; use the escort service after dark",
            "sign up for emergency alerts so you're in the loop",
        ],
    },
]


def _match_topics(text: str) -> list[dict]:
    found = []
    for tpl in TOPIC_TEMPLATES:
        for pat in tpl["patterns"]:
            if re.search(pat, text, flags=re.I):
                found.append(tpl)
                break
    if not found:
        found = [random.choice(TOPIC_TEMPLATES)]
    random.shuffle(found)
    return found


def _dedup_pairs(pairs: list[dict], threshold: int = 90) -> list[dict]:
    deduped: list[dict] = []
    seen: list[str] = []
    for p in pairs:
        sig = f"{p['instruction']}||{p['output']}"
        if any(fuzz.partial_ratio(sig, s) >= threshold for s in seen):
            continue
        seen.append(sig)
        deduped.append(p)
    return deduped


def generate_from_page(text: str, url: str, cfg: QAGeneratorConfig) -> list[dict]:
    sentences = split_sentences(text)[:200]
    joined = " ".join(sentences[:40])
    topics = _match_topics(joined)

    pairs: list[dict] = []
    for tpl in topics:
        for _ in range(3):
            q = random.choice(tpl["instructions"])
            a = random.choice(tpl["answers"]).rstrip(".")
            a = f"{a}. ({url})"
            a = _voiceify(a)
            pairs.append({"instruction": q, "output": a})
            if len(pairs) >= cfg.max_pairs_per_page:
                break
        if len(pairs) >= cfg.max_pairs_per_page:
            break

    return _dedup_pairs(pairs)


def generate_from_reddit(text: str, url: str, cfg: QAGeneratorConfig) -> list[dict]:
    sentences = split_sentences(text)
    if not sentences:
        return []
    picks = sentences[: min(5, len(sentences))]
    pairs = []
    for s in picks:
        instr = s
        if len(instr) > 120:
            instr = instr[:118] + "…"
        answer = "community says: " + s
        answer = _voiceify(answer)
        answer = f"{answer} ({url})"
        pairs.append({"instruction": instr, "output": answer})
        if len(pairs) >= cfg.max_pairs_from_reddit_post:
            break
    return pairs


def build_dataset(items: Iterable[dict], cfg: QAGeneratorConfig, max_total: int | None = None) -> list[dict]:
    all_pairs: list[dict] = []
    for it in items:
        url = it.get("url", "")
        src = it.get("source", "web")
        text = clean_text(it.get("text", ""))
        if not text:
            continue
        if src.startswith("reddit"):
            pairs = generate_from_reddit(text, url, cfg)
        else:
            pairs = generate_from_page(text, url, cfg)
        all_pairs.extend(pairs)
        if max_total and len(all_pairs) >= max_total:
            break
    random.shuffle(all_pairs)
    if max_total:
        all_pairs = all_pairs[:max_total]
    return _dedup_pairs(all_pairs)