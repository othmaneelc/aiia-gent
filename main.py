import os
import json
import yaml

from utils_time import is_send_window, today_local_str
from news_collect import fetch_rss_items, fetch_arxiv, dedupe_items, rank_items
from digest import format_short, format_medium, format_deep, build_email_body
from send_email import send_gmail

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_sent_date": None}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_sources():
    with open("sources.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    # 1) Only send during Morocco 08:00 window
    if not is_send_window(8, 0, 14):
        print("Not in send window. Exiting.")
        return

    today = today_local_str()
    state = load_state()

    if state.get("last_sent_date") == today:
        print("Already sent today. Exiting.")
        return

    sources = load_sources()

    # 2) Collect
    print("Collecting news...")
    items = []
    items += fetch_rss_items(sources.get("rss", []))
    for cat in sources.get("arxiv", []):
        items += fetch_arxiv(cat)

    # 3) Dedupe + rank
    items = dedupe_items(items)
    items = rank_items(items)
    print(f"Found {len(items)} unique items.")

    # 4) Build digest (no AI summaries — titles only, clean and reliable)
    short = format_short(items, n=5)
    medium = format_medium(items, n=10)
    deep = format_deep(items, n=15)
    body = build_email_body(today, short, medium, deep)

    # 5) Send email
    sender = os.environ["GMAIL_SENDER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["EMAIL_RECIPIENT"]
    subject = f"AI Daily Brief — {today} (Morocco)"

    send_gmail(sender, app_password, recipient, subject, body)
    print("Email sent.")

    # 6) Mark sent
    state["last_sent_date"] = today
    save_state(state)
    print("Done.")


if __name__ == "__main__":
    main()
