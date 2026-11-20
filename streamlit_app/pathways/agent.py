"""The seam between the UI and the backend agent.

The UI only ever talks to an ``AgentClient``. Today that is ``MockAgent`` (canned, fictional answers so
the whole experience can be demoed with no credentials). Later it will be ``SalesforceAgent``, which
calls the Agentforce Agent API. Swapping is one line in ``get_agent`` and nothing in the UI changes.
"""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass, field
from typing import Protocol

from . import content


# ---- Data passed between the agent and the UI ---------------------------------------------------------
@dataclass
class AgentReply:
    """One assistant turn.

    text:         the message bubble (markdown allowed)
    cards:        optional rich cards, each ``{"kind": ..., "data": {...}}``; kinds the UI knows:
                  "program", "sources", "status", "handoff_sent"
    action:       ``None``, ``"verify"`` (open the ID check) or ``"handoff"`` (open the request form)
    suggestions:  follow-up questions to show as chips; empty means "use the defaults"
    """

    text: str
    cards: list[dict] = field(default_factory=list)
    action: str | None = None
    suggestions: list[str] = field(default_factory=list)


@dataclass
class VerifyResult:
    ok: bool
    name: str = ""
    message: str = ""


@dataclass
class HandoffResult:
    reference: str
    message: str


class AgentClient(Protocol):
    def send(self, text: str, *, verified: bool) -> AgentReply: ...

    def verify(self, email: str, application_id: str) -> VerifyResult: ...

    def application_status(self) -> AgentReply: ...

    def request_handoff(
        self, topic: str, best_time: str, contact: str, note: str, transcript: list[dict]
    ) -> HandoffResult: ...


class AgentUnavailable(Exception):
    """Raised by a backend when it cannot answer. The UI turns it into the friendly error state."""


# ---- Mock agent (default) ---------------------------------------------------------------------------------
def _program_card() -> dict:
    return {"kind": "program", "data": content.DEMO_PROGRAM}


def _sources_card() -> dict:
    return {"kind": "sources", "data": {"items": content.DEMO_SOURCES}}


class MockAgent:
    """Keyword-routed, fully fictional. Good enough to exercise every screen and state."""

    def __init__(self, latency: float | None = None) -> None:
        if latency is None:
            latency = float(os.environ.get("PATHWAYS_MOCK_LATENCY", "1.1"))
        self.latency = latency

    def _wait(self, factor: float = 1.0) -> None:
        if self.latency > 0:
            time.sleep(self.latency * factor)

    def send(self, text: str, *, verified: bool) -> AgentReply:
        self._wait()
        t = text.lower()

        if "simulate error" in t:  # lets you demo the error state: type "simulate error"
            raise AgentUnavailable("simulated failure")
        if re.search(r"\b(person|human|advisor|someone|agent|talk|speak|call me)\b", t):
            return AgentReply(
                "Of course. Tell me a little and an advisor will follow up with you.",
                action="handoff",
            )
        if re.search(r"more time|extension|extend|deadline", t):
            return AgentReply(
                "Extensions are decided by an advisor, who can look at your situation. "
                "I can set up a follow-up for you if you'd like.",
                suggestions=["Talk to an advisor", "What documents are accepted?"],
            )
        if re.search(r"\bapplication\b|\bstatus\b", t):
            if verified:
                return self.application_status()
            return AgentReply(
                "I can look that up as soon as I've confirmed it's you. It only takes a moment.",
                action="verify",
            )
        if re.search(r"document|diploma|\bged\b|accepted", t):
            return AgentReply(
                "A high school diploma or GED, plus a government-issued photo ID. "
                "Uploads happen in your applicant portal.",
                cards=[_sources_card()],
                suggestions=["Can I get more time?", "Talk to an advisor"],
            )
        if re.search(r"typical week|schedule|per week|week look", t):
            return AgentReply(
                "Evening classes, about three sessions a week, plus a little time for practice labs.",
                suggestions=["Can I start in January?", "What do I need to apply?", "Talk to an advisor"],
            )
        if re.search(r"cost|tuition|price|\bfee|\bpay\b", t):
            return AgentReply(
                "Costs vary by program, and many are fully funded for eligible applicants. "
                "An advisor can confirm what applies to you.",
                suggestions=["What do I need to apply?", "Talk to an advisor"],
            )
        if re.search(r"january|\bstart\b|cohort|\bwhen\b|\bstarts\b", t):
            return AgentReply(
                "The next IT Support Specialist cohort starts January 11.",
                cards=[_program_card()],
                suggestions=["What does a typical week look like?", "What do I need to apply?"],
            )
        if re.search(r"what programs|which programs|explore programs|(programs?|courses?).*\boffer|\boffer\b.*programs?", t):
            return AgentReply(
                "This simulation covers one program, IT Support Specialist. Here's a quick overview.",
                cards=[_program_card(), _sources_card()],
                suggestions=["What do I need to apply?", "Can I start in January?", "What does a typical week look like?"],
            )
        if re.search(r"apply|program|admission|requirement|explore|offer|learn", t):
            return AgentReply(
                "To apply for IT Support Specialist you'll need a high school diploma or GED, a "
                "government-issued photo ID, and a short intake call. No prior IT experience is required.",
                cards=[_program_card(), _sources_card()],
                suggestions=["Can I start in January?", "What does a typical week look like?", "Talk to an advisor"],
            )
        return AgentReply(
            "In this simulation I can help with programs and admissions, check where your application "
            "stands, or connect you with an advisor.",
            suggestions=list(content.DEFAULT_SUGGESTIONS),
        )

    def verify(self, email: str, application_id: str) -> VerifyResult:
        self._wait(0.6)
        if (
            email.strip().lower() == content.DEMO_EMAIL
            and application_id.strip().upper() == content.DEMO_APPLICATION_ID
        ):
            return VerifyResult(ok=True, name=content.DEMO_NAME)
        return VerifyResult(
            ok=False,
            message="I couldn't match those details to an application. Check the email and ID, or ask for a person.",
        )

    def application_status(self) -> AgentReply:
        self._wait(1.4)
        return AgentReply(
            f"Thanks, {content.DEMO_NAME}, you're verified. Here's where your application stands.",
            cards=[
                {
                    "kind": "status",
                    "data": {
                        "program": content.DEMO_PROGRAM["name"],
                        "application_id": content.DEMO_APPLICATION_ID,
                        "stages": content.DEMO_STAGES,
                        "current": content.DEMO_CURRENT_STAGE,
                        "next_step": content.DEMO_NEXT_STEP,
                    },
                }
            ],
            suggestions=["What documents are accepted?", "Can I get more time?", "Talk to an advisor"],
        )

    def request_handoff(
        self, topic: str, best_time: str, contact: str, note: str, transcript: list[dict]
    ) -> HandoffResult:
        self._wait(0.8)
        return HandoffResult(
            reference=content.DEMO_HANDOFF_REFERENCE,
            message=f"By {contact.lower()}, {best_time.lower()}, within 1 business day.",
        )


# ---- Salesforce agent (stub, filled in after the design is approved) -----------------------------------------
class SalesforceAgent:
    """TODO(salesforce): Agentforce Agent API integration.

    Outline, to verify against the current Salesforce docs before building:
      1. Auth: OAuth client-credentials flow against the org's My Domain URL, with the token cached
         (``st.cache_resource``) and refreshed on expiry.
      2. Start a session for ``agent_id`` once per Streamlit session and keep the session id in
         ``st.session_state``.
      3. ``send``: post the user's text to the session, then map the response onto ``AgentReply``.
         Verification and handoff should come back as explicit signals (for example an action or topic
         in the agent's response) so ``action`` is set without keyword guessing in the UI.
      4. ``verify`` and ``request_handoff`` should call the agent's actions, never trust client-side checks.
      5. End the session when the chat is reset.
    Credentials come from ``st.secrets["salesforce"]`` (see ``.streamlit/secrets.toml.example``).
    """

    def __init__(self, settings: dict) -> None:
        self.settings = settings

    def send(self, text: str, *, verified: bool) -> AgentReply:
        raise NotImplementedError("TODO(salesforce): call the Agent API")

    def verify(self, email: str, application_id: str) -> VerifyResult:
        raise NotImplementedError("TODO(salesforce): call the verification action")

    def application_status(self) -> AgentReply:
        raise NotImplementedError("TODO(salesforce): fetch status through the agent")

    def request_handoff(
        self, topic: str, best_time: str, contact: str, note: str, transcript: list[dict]
    ) -> HandoffResult:
        raise NotImplementedError("TODO(salesforce): create the follow-up case")


def get_agent() -> AgentClient:
    """Pick the backend. Defaults to the mock so the app always runs without credentials."""
    backend = os.environ.get("PATHWAYS_BACKEND", "mock").lower()
    if backend == "salesforce":
        import streamlit as st

        return SalesforceAgent(dict(st.secrets["salesforce"]))
    return MockAgent()
