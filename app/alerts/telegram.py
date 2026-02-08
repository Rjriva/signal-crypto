from __future__ import annotations

import json
import os
from pathlib import Path
import requests


STATE_FILE = Path("state.json")


def send_telegram_alert(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})


def alert_if_new(signal_key: str, message: str):
    state = {}
    if STATE_FILE.exists():
        state = json.loads(STATE_FILE.read_text())

    if state.get(signal_key) != message:
        send_telegram_alert(message)
        state[signal_key] = message
        STATE_FILE.write_text(json.dumps(state))