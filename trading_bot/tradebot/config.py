"""Settings loaded from config.yaml (non-secret) and .env / environment (secrets).

Secrets never live in config.yaml:
  ANTHROPIC_API_KEY   Claude (or an `ant auth login` profile)
  FMP_API_KEY         Financial Modeling Prep
  XAI_API_KEY         Grok, only if the Grok scout is enabled
  TRADEBOT_WEBHOOK_URL  optional Slack/Discord-style webhook for notifications
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import ClassVar, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

Effort = Literal["low", "medium", "high", "xhigh", "max"]


class _Cfg(BaseModel):
    # Typos in config.yaml should fail loudly instead of silently using a default.
    model_config = ConfigDict(extra="forbid")


ProviderName = Literal["claude", "openai", "grok", "claude_cli", "codex_cli", "fake"]

# USD per 1mn tokens (input, output), used to log what each call cost or would have cost on the
# API. Anthropic: claude.com/pricing and the API docs; OpenAI GPT-6: OpenAI pricing page (2026-09);
# Grok: press reports (2026-09). Update here when prices change.
DEFAULT_PRICES: dict[str, list[float]] = {
    "claude-fable-5-1": [10.0, 50.0],
    "claude-opus-5-5": [4.0, 20.0],
    "claude-opus-5": [5.0, 25.0],
    "claude-sonnet-5": [2.0, 10.0],
    "claude-haiku-4-5": [1.0, 5.0],
    "gpt-6-astra": [10.0, 50.0],
    "gpt-6-sol": [2.0, 10.0],
    "gpt-6-luna": [0.1, 0.5],
    "grok-4.7": [2.0, 6.0],
}


class LLMTask(_Cfg):
    """Which provider and model handle one stage of the pipeline."""

    provider: ProviderName = "claude"
    model: str = "claude-opus-5"
    effort: Effort | None = None
    max_tokens: int = 16000
    # Used only when this task's subscription window or API quota is used up.
    fallback: LLMTask | None = None


class CLIConfig(_Cfg):
    """How the subscription providers call the official command-line tools."""

    claude_path: str = "claude"
    codex_path: str = "codex"
    timeout_minutes: int = 30
    # Remove API keys from the CLI's environment so it bills your subscription, not the API.
    use_subscription_login: bool = True
    # After a "usage limit reached" error, deep dives wait this long before trying again.
    pause_minutes_on_limit: int = 60
    # Models used by `tradebot compare` for each route.
    claude_model: str = "opus"
    codex_model: str = "gpt-6-astra"


class LLMConfig(_Cfg):
    # Default = the hybrid plan: always-on, time-sensitive stages on a cheap API model; the heavy,
    # batchable deep dive on a subscription CLI.
    triage: LLMTask = Field(default_factory=lambda: LLMTask(provider="openai", model="gpt-6-luna", effort="low"))
    industry: LLMTask = Field(default_factory=lambda: LLMTask(provider="openai", model="gpt-6-sol", effort="medium"))
    screen: LLMTask = Field(default_factory=lambda: LLMTask(provider="openai", model="gpt-6-sol", effort="medium"))
    research: LLMTask = Field(default_factory=lambda: LLMTask(provider="claude_cli", model="opus", effort="high"))
    synthesis: LLMTask = Field(default_factory=lambda: LLMTask(provider="claude_cli", model="opus", effort="high"))
    thesis: LLMTask = Field(default_factory=lambda: LLMTask(provider="openai", model="gpt-6-sol", effort="medium"))
    scout: LLMTask = Field(default_factory=lambda: LLMTask(provider="grok", model="grok-4.7"))
    web_search_max_uses: int = 12
    language: str = "Simplified Chinese"
    cli: CLIConfig = Field(default_factory=CLIConfig)
    prices: dict[str, list[float]] = Field(default_factory=lambda: dict(DEFAULT_PRICES))

    STAGES: ClassVar[tuple[str, ...]] = ("triage", "industry", "screen", "research", "synthesis", "thesis", "scout")

    def providers_in_use(self, include_scout: bool) -> set[str]:
        names: set[str] = set()
        for stage in self.STAGES:
            if stage == "scout" and not include_scout:
                continue
            task: LLMTask | None = getattr(self, stage)
            while task is not None:
                names.add(task.provider)
                task = task.fallback
        return names


class UniverseConfig(_Cfg):
    # v1 trades US-listed stocks and ADRs only (TSM, ASML, CDNS, ...), priced in USD.
    min_market_cap_usd: float = 2_000_000_000
    min_price: float = 5.0
    exclude: list[str] = Field(default_factory=list)
    watchlist: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)


class ScheduleConfig(_Cfg):
    news_poll_minutes: int = 15
    daily_scan_hour_utc: int = 12
    max_deep_dives_per_day: int = 3
    # A deep dive can take tens of minutes; doing one per cycle keeps news triage running in between.
    deep_dives_per_cycle: int = 1
    top_industries: int = 5
    candidates_per_industry: int = 2
    approval_ttl_hours: int = 24


class ResearchConfig(_Cfg):
    agents_dir: str = "../.claude/agents"
    notes_dir: str = "data/research"
    open_conviction: int = 70
    exit_conviction: int = 50
    full_conviction: int = 95
    exit_on_broken_pillars: int = 2
    allowed_verdicts: list[str] = Field(default_factory=lambda: ["PASS", "PASS_WITH_MINOR_REVISIONS"])
    materiality_threshold: int = 6
    max_revision_rounds: int = 1
    max_docs: int = 6
    max_doc_chars: int = 150_000


class RiskConfig(_Cfg):
    trading_enabled: bool = True
    long_only: bool = True
    max_position_pct: float = 8.0
    max_industry_pct: float = 30.0
    max_gross_leverage: float = 1.0
    max_positions: int = 15
    max_orders_per_day: int = 10
    max_daily_loss_pct: float = 3.0
    max_price_deviation_pct: float = 3.0
    min_order_value: float = 1_000.0
    rebalance_band_pct: float = 1.5
    require_compliance_cleared: bool = True


class ExecutionConfig(_Cfg):
    broker: Literal["paper", "ibkr"] = "paper"
    approval: Literal["manual", "auto"] = "manual"
    auto_approve_exits: bool = False
    limit_offset_pct: float = 0.3
    paper_starting_cash: float = 1_000_000.0
    ibkr_host: str = "127.0.0.1"
    ibkr_port: int = 7497  # 7497 = TWS paper, 4002 = Gateway paper; 7496 / 4001 are LIVE
    ibkr_client_id: int = 17
    allow_live: bool = False


class SourcesConfig(_Cfg):
    fmp_news: bool = True
    grok_scout: bool = False
    grok_x_handles: list[str] = Field(default_factory=list)
    inbox_dir: str = "inbox"


class Settings(_Cfg):
    data_dir: str = "data"
    universe: UniverseConfig = Field(default_factory=UniverseConfig)
    schedule: ScheduleConfig = Field(default_factory=ScheduleConfig)
    research: ResearchConfig = Field(default_factory=ResearchConfig)
    risk: RiskConfig = Field(default_factory=RiskConfig)
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    sources: SourcesConfig = Field(default_factory=SourcesConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    # Directory that relative paths resolve against: the folder holding config.yaml.
    base_dir: Path = Field(default_factory=Path.cwd, exclude=True)

    def path(self, value: str) -> Path:
        p = Path(value).expanduser()
        return p if p.is_absolute() else (self.base_dir / p).resolve()

    @property
    def data_path(self) -> Path:
        return self.path(self.data_dir)

    @property
    def db_path(self) -> Path:
        return self.data_path / "tradebot.db"

    @property
    def stop_file(self) -> Path:
        return self.data_path / "STOP"


def load_env_file(path: Path) -> None:
    """Minimal .env reader (KEY=VALUE per line). Real environment variables win."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_settings(path: str | Path = "config.yaml") -> Settings:
    config_path = Path(path).expanduser().resolve()
    raw = {}
    if config_path.exists():
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    settings = Settings.model_validate(raw)
    settings.base_dir = config_path.parent
    load_env_file(settings.base_dir / ".env")
    return settings
