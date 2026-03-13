def format_short(items, n=5):
    lines = []
    for i, it in enumerate(items[:n], 1):
        lines.append(f"{i}. {it['title']}\n{it['url']}")
    return "\n\n".join(lines)


def format_medium(items, n=10):
    lines = []
    for i, it in enumerate(items[:n], 1):
        lines.append(
            f"{i}) {it['title']}\n"
            f"Source: {it['source']}\n"
            f"Link: {it['url']}\n"
        )
    return "\n".join(lines)


def format_deep(items, n=15):
    lines = []
    lines.append("--- TOP STORIES ---\n")
    for i, it in enumerate(items[:n], 1):
        lines.append(
            f"{i}) {it['title']}\n"
            f"- Source: {it['source']}\n"
            f"- Link: {it['url']}\n"
        )
    return "\n".join(lines)


def build_email_body(date_str, short, medium, deep):
    return f"""AI Daily Brief — {date_str} (Morocco)
========================
SHORT (quick scan)
========================
{short}

========================
MEDIUM (more context)
========================
{medium}

========================
DEEP DIVE (full list)
========================
{deep}
"""
