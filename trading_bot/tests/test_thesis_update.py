from conftest import make_thesis

from tradebot.models import PillarUpdate, ThesisAssessment, utcnow
from tradebot.research.deep_dive import parse_verdict
from tradebot.research.thesis_update import apply_assessment


def assessment(**overrides) -> ThesisAssessment:
    fields = dict(pillar_updates=[], kill_criteria_hit=[], conviction_delta=0, note="n", needs_full_refresh=False)
    fields.update(overrides)
    return ThesisAssessment(**fields)


def apply(settings, thesis, a):
    return apply_assessment(thesis, a, "news-1", settings.research, utcnow())


def test_routine_news_moves_conviction_a_little(settings):
    updated = apply(settings, make_thesis(conviction=80), assessment(conviction_delta=-3))
    assert updated.conviction == 77 and updated.status == "active"
    assert updated.history[-1].conviction_before == 80


def test_upside_is_capped(settings):
    assert apply(settings, make_thesis(conviction=80), assessment(conviction_delta=40)).conviction == 95


def test_kill_criterion_closes_thesis(settings):
    updated = apply(settings, make_thesis(conviction=85), assessment(kill_criteria_hit=[0]))
    assert updated.conviction == 0 and updated.status == "closed"
    assert "customer leaves" in updated.history[-1].note


def test_out_of_range_indexes_are_ignored(settings):
    updated = apply(settings, make_thesis(conviction=80), assessment(
        kill_criteria_hit=[7], pillar_updates=[PillarUpdate(index=9, status="broken", reason="x")]))
    assert updated.conviction == 80 and updated.status == "active"


def test_two_broken_pillars_force_exit(settings):
    updates = [PillarUpdate(index=i, status="broken", reason="x") for i in (0, 1)]
    updated = apply(settings, make_thesis(conviction=80), assessment(pillar_updates=updates, conviction_delta=-5))
    assert updated.conviction == 49 and updated.status == "closed"


def test_watch_thesis_can_be_upgraded(settings):
    updated = apply(settings, make_thesis(status="watch", conviction=66), assessment(conviction_delta=6))
    assert updated.status == "active"
    rejected = apply(settings, make_thesis(status="watch", conviction=66, reviewer_verdict="REJECT"),
                     assessment(conviction_delta=6))
    assert rejected.status == "watch"


def test_parse_verdict():
    assert parse_verdict("...\n\nVERDICT: PASS WITH MINOR REVISIONS") == "PASS_WITH_MINOR_REVISIONS"
    assert parse_verdict("options: PASS / REJECT\n**VERDICT：** REVISE AND RESUBMIT") == "REVISE_AND_RESUBMIT"
    assert parse_verdict("verdict: pass") == "PASS"
    assert parse_verdict("no verdict line here") is None
