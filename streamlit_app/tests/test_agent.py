"""Unit tests for the mock agent (no Streamlit involved)."""

import pytest

from pathways import content
from pathways.agent import AgentUnavailable, MockAgent, get_agent


@pytest.fixture
def agent() -> MockAgent:
    return MockAgent(latency=0)


def test_default_backend_is_mock(monkeypatch):
    monkeypatch.delenv("PATHWAYS_BACKEND", raising=False)
    assert isinstance(get_agent(), MockAgent)


def test_explore_message_says_one_program_and_shows_it(agent):
    reply = agent.send(content.EXPLORE_MESSAGE, verified=False)
    kinds = [c["kind"] for c in reply.cards]
    assert "program" in kinds and "sources" in kinds
    assert "one program" in reply.text
    assert reply.action is None


def test_requirements_question_still_gets_requirements(agent):
    reply = agent.send("What do I need to apply?", verified=False)
    assert "diploma" in reply.text.lower()


def test_status_requires_verification_first(agent):
    reply = agent.send(content.STATUS_MESSAGE, verified=False)
    assert reply.action == "verify"
    assert reply.cards == []


def test_status_when_verified_returns_status_card(agent):
    reply = agent.send(content.STATUS_MESSAGE, verified=True)
    assert reply.cards and reply.cards[0]["kind"] == "status"
    assert reply.action is None


def test_human_message_opens_handoff(agent):
    reply = agent.send(content.HUMAN_MESSAGE, verified=False)
    assert reply.action == "handoff"


def test_verify_accepts_demo_credentials_only(agent):
    ok = agent.verify(content.DEMO_EMAIL, content.DEMO_APPLICATION_ID)
    assert ok.ok and ok.name == content.DEMO_NAME
    bad = agent.verify("someone@else.com", "APP-00000")
    assert not bad.ok and bad.message


def test_verify_is_forgiving_about_case_and_spaces(agent):
    assert agent.verify("  JORDAN.M@email.com ", " app-00482 ").ok


def test_handoff_returns_reference(agent):
    result = agent.request_handoff("My application", "Weekday mornings", "Email", "", [])
    assert result.reference == content.DEMO_HANDOFF_REFERENCE
    assert "weekday mornings" in result.message


def test_unknown_question_gets_a_fallback_with_suggestions(agent):
    reply = agent.send("what is the airspeed of a swallow", verified=False)
    assert reply.text
    assert reply.suggestions


def test_simulate_error_raises(agent):
    with pytest.raises(AgentUnavailable):
        agent.send("please simulate error", verified=False)
