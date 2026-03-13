import feedparser
import requests
from datetime import datetime, timedelta, timezone


def fetch_rss_items(feed_urls, max_items_per_feed=20):
    items = []
    for url in feed_urls:
        parsed = feedparser.parse(url)
        for e in parsed.entries[:max_items_per_feed]:
            title = (e.get("title") or "").strip()
            link = (e.get("link") or "").strip()
            published = e.get("published") or e.get("updated") or ""
            items.append({
                "source": url,
                "title": title,
                "url": link,
                "published": published
            })
    return items


def fetch_arxiv(cat, max_results=15):
    # arXiv API returns Atom
    base = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{cat}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    r = requests.get(base, params=params, timeout=30)
    r.raise_for_status()
    parsed = feedparser.parse(r.text)
    items = []
    for e in parsed.entries:
        title = (e.get("title") or "").replace("\n", " ").strip()
        link = ""
        for l in e.get("links", []):
            if l.get("rel") == "alternate":
                link = l.get("href", "")
                break
        items.append({
            "source": f"arXiv:{cat}",
            "title": title,
            "url": link,
            "published": e.get("published", "")
        })
    return items


def normalize_title(t):
    return " ".join((t or "").lower().split())


def dedupe_items(items):
    seen = set()
    out = []
    for it in items:
        key = normalize_title(it.get("title"))[:160]
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out


def score_item(it):
    title = (it.get("title") or "").lower()
    # Simple keyword-based scoring (you can tune this later)
    keywords = [
        ("release", 4), ("launch", 4), ("introduces", 3), ("announces", 3),
        ("paper", 2), ("benchmark", 3), ("sota", 3), ("agent", 2),
        ("robot", 2), ("regulation", 3), ("policy", 2), ("security", 3),
        ("openai", 3), ("anthropic", 3), ("deepmind", 3), ("nvidia", 3),
        ("llm", 2), ("reasoning", 2), ("model", 2),
    ]
    score = 0
    for k, w in keywords:
        if k in title:
            score += w
    # Source credibility weight (rough)
    src = (it.get("source") or "").lower()
    if "arxiv" in src:
        score += 2
    if "techcrunch" in src or "theverge" in src or "arstechnica" in src or "venturebeat" in src:
        score += 2
    return score


def rank_items(items):
    return sorted(items, key=score_item, reverse=True)
