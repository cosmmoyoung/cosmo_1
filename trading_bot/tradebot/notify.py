"""Notifications: always logged; also posted to a webhook when TRADEBOT_WEBHOOK_URL is set."""

from __future__ import annotations

import logging

import requests

log = logging.getLogger("tradebot.notify")


class Notifier:
    def __init__(self, webhook_url: str | None = None):
        self.webhook_url = webhook_url
        self.sent: list[str] = []

    def send(self, title: str, body: str = "") -> None:
        message = f"{title}\n{body}".strip()
        self.sent.append(message)
        log.info(message)
        if not self.webhook_url:
            return
        try:
            # "text" is read by Slack-style hooks, "content" by Discord-style hooks.
            requests.post(self.webhook_url, json={"text": message, "content": message}, timeout=10)
        except requests.RequestException as exc:
            log.warning("webhook failed: %s", exc)
