"""加载 config.yaml 和环境变量,给全流水线提供统一配置入口。"""
import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _load_dotenv() -> None:
    """极简 .env 加载器,避免引入额外依赖。已存在的环境变量优先。"""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if key and value and key not in os.environ:
            os.environ[key] = value


def load_config() -> dict:
    _load_dotenv()
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["env"] = {
        "anthropic_key": os.environ.get("ANTHROPIC_API_KEY", ""),
        "fmp_key": os.environ.get("FMP_API_KEY", ""),
        "x_bearer": os.environ.get("X_BEARER_TOKEN", ""),
        "telegram_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "telegram_chat": os.environ.get("TELEGRAM_CHAT_ID", ""),
    }
    return cfg
