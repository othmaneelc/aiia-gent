import requests


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # Free tier, fast


def _call_groq(prompt: str, max_tokens: int = 150) -> str:
    import os
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return ""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    r = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def summarize_items(items: list, n: int = 10) -> list:
    summarized = []
    for it in items[:n]:
        title = it.get("title", "")
        source = it.get("source", "")

        prompt = f"""You are an AI news analyst writing for a sharp, no-fluff tech newsletter.

Article title: {title}
Source: {source}

Write exactly 2 sentences:
1. What this is about (the core fact or finding).
2. Why it matters for AI builders, founders, or researchers.

Be direct. No hype. No filler. Max 60 words total."""

        try:
            summary = _call_groq(prompt, max_tokens=150)
        except Exception as e:
            summary = f"(Summary unavailable: {e})"

        summarized.append({**it, "summary": summary})

    return summarized


def generate_theme(items: list) -> str:
    titles = "\n".join(f"- {it.get('title', '')}" for it in items[:15])
    prompt = f"""You are an AI trends analyst. Here are today's top AI headlines:

{titles}

In 1-2 sentences, identify the single biggest theme or pattern across these stories.
Be specific and insightful. Max 50 words."""

    try:
        return _call_groq(prompt, max_tokens=100)
    except Exception as e:
        return f"(Theme unavailable: {e})"
