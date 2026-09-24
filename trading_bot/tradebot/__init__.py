"""tradebot: a thesis-driven research and trading bot.

News and documents flow through a funnel: triage -> industry scan -> company
screen -> deep dive (researcher -> critic -> reviewer -> PM synthesis). A thesis
that survives becomes an order proposal, which must pass hard-coded risk rules
and (by default) a human approval before it reaches the broker. Every new piece
of news is re-checked against the open theses, which can trim or exit positions.
"""

__version__ = "0.1.0"
