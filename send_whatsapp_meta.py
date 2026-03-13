import requests


def send_whatsapp_text(access_token, phone_number_id, to_number, message_text):
    """
    Meta WhatsApp Cloud API: send a plain text message.
    to_number must be in international format, e.g. "2126XXXXXXXX" (no +).
    """
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text[:3900]}  # keep within safe length
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()
