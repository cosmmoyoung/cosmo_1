"""推送渠道:Telegram(免费、最简单)和邮件。都没配置就只留文件。"""
import os
import smtplib
from email.mime.text import MIMEText

import requests


def notify(cfg: dict, run_date: str, report_text: str) -> None:
    sent = False
    if cfg["notify"].get("telegram") and cfg["env"]["telegram_token"]:
        sent = _send_telegram(cfg, report_text) or sent
    if cfg["notify"].get("email") and os.environ.get("SMTP_HOST"):
        sent = _send_email(run_date, report_text) or sent
    if not sent:
        print("[info] 未配置推送渠道,报告已保存为本地文件。")


def _send_telegram(cfg: dict, text: str) -> bool:
    # Telegram 单条消息上限 4096 字符,超长时分段发
    token, chat = cfg["env"]["telegram_token"], cfg["env"]["telegram_chat"]
    try:
        for i in range(0, len(text), 3800):
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat, "text": text[i:i + 3800]},
                timeout=30,
            ).raise_for_status()
        print("[ok] 已推送到 Telegram")
        return True
    except Exception as e:
        print(f"[warn] Telegram 推送失败: {e}")
        return False


def _send_email(run_date: str, text: str) -> bool:
    try:
        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = f"市场监测晨报 {run_date}"
        msg["From"] = os.environ["SMTP_USER"]
        msg["To"] = os.environ["EMAIL_TO"]
        with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as s:
            s.starttls()
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            s.send_message(msg)
        print("[ok] 已发送邮件")
        return True
    except Exception as e:
        print(f"[warn] 邮件发送失败: {e}")
        return False
