"""Streamlit layout and interaction logic. Styling lives in theme.py, copy in content.py, backend in agent.py."""

from __future__ import annotations

import re
import uuid

import streamlit as st

from . import cards, content, theme
from .agent import AgentClient, AgentReply, get_agent

# ---- State -----------------------------------------------------------------------------------------------------


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("messages", [])  # [{"role", "text", "cards", "action", "suggestions", ...}]
    ss.setdefault("pending", None)  # {"kind": "send", "text": ...} or {"kind": "lookup"}
    ss.setdefault("verified", None)  # {"name", "email", "application_id"} once the ID check passes
    ss.setdefault("awaiting", None)  # "verify" or "handoff" while the agent is waiting on a form
    ss.setdefault("dialog", None)  # one-shot request to open a dialog on the next run
    ss.setdefault("session_id", uuid.uuid4().hex)
    ss.setdefault("scrolled_to", 0)


def reset_chat() -> None:
    ss = st.session_state
    ss.messages = []
    ss.pending = None
    ss.verified = None
    ss.awaiting = None
    ss.dialog = None
    ss.scrolled_to = 0
    ss.session_id = uuid.uuid4().hex


def queue_message(text: str) -> None:
    """Add the user's message and ask the next run to fetch the reply. Used as an on_click callback."""
    ss = st.session_state
    ss.messages.append({"role": "user", "text": text})
    ss.pending = {"kind": "send", "text": text}
    ss.awaiting = None


def _open_dialog(name: str) -> None:
    st.session_state.dialog = name


def _retry(payload: dict) -> None:
    ss = st.session_state
    if ss.messages and ss.messages[-1].get("error"):
        ss.messages.pop()
    ss.pending = payload


@st.cache_resource
def get_cached_agent() -> AgentClient:
    return get_agent()


def inject_theme() -> None:
    st.html(f"<style>{theme.build_css()}</style>")


_MD_SPECIALS = re.compile(r"([\\`*_{}\[\]()#+\-.!|>~<])")


def _plain(text: str) -> str:
    """Show user-typed text literally (no markdown formatting)."""
    return _MD_SPECIALS.sub(r"\\\1", text)


# ---- Header and home ------------------------------------------------------------------------------------------


def render_header(in_chat: bool) -> None:
    # TODO(post-MVP): optional header pills on the right, "Not verified · Sign in" and "Talk to a person".
    # The sign-in pill needs an auth callback from Salesforce to flip to "Verified", so it is parked on
    # purpose. The tiles and in-chat dialogs already cover both journeys.
    with st.container(key="head"):
        st.html(cards.brand_html())
        if in_chat:
            st.button("New chat", key="new_chat", on_click=reset_chat)


def _composer(where: str, placeholder: str) -> None:
    def submit() -> None:
        text = (st.session_state.get(f"msg_{where}") or "").strip()
        if text:
            queue_message(text)

    with st.form(f"form_{where}", clear_on_submit=True):
        st.text_input(
            "Message Pathways", key=f"msg_{where}", placeholder=placeholder, label_visibility="collapsed"
        )
        st.form_submit_button("Send", type="primary", on_click=submit)


def render_home() -> None:
    st.html(cards.hero_html(content.HERO_TITLE, content.HERO_BODY))
    with st.container(key="composer_home"):
        _composer("home", content.COMPOSER_PLACEHOLDER_HOME)
        with st.container(key="chips_home"):
            for i, label in enumerate(content.HOME_SUGGESTIONS):
                st.button(label, key=f"chip_home_{i}", on_click=queue_message, args=(label,))
    columns = st.columns(len(content.TILES), gap="medium")
    for column, tile in zip(columns, content.TILES):
        with column:
            st.button(tile["title"], key=f"tile_{tile['key']}", on_click=queue_message, args=(tile["message"],))


# ---- Conversation -------------------------------------------------------------------------------------------------


def _render_assistant(i: int, msg: dict, is_last: bool) -> None:
    with st.container(key=f"turn_asst_{i}"):
        if msg.get("error"):
            with st.container(key=f"bub_err_{i}"):
                st.html(cards.error_html(msg["reference"]))
            if is_last:
                st.button("Try again", key=f"retry_{i}", type="primary", on_click=_retry, args=(msg["retry"],))
                st.button(
                    "Talk to a person", key=f"err_human_{i}", on_click=queue_message, args=(content.HUMAN_MESSAGE,)
                )
            return
        with st.container(key=f"bub_asst_{i}"):
            st.markdown(msg["text"])
        for card in msg.get("cards", []):
            st.html(cards.render_card(card))
        if not is_last:
            return
        awaiting = st.session_state.awaiting
        if awaiting == "verify":
            st.button("Verify it's you", key=f"open_verify_{i}", type="primary", on_click=_open_dialog, args=("verify",))
        elif awaiting == "handoff":
            st.button("Open request form", key=f"open_handoff_{i}", type="primary", on_click=_open_dialog, args=("handoff",))
        if any(c["kind"] == "handoff_sent" for c in msg.get("cards", [])):
            st.button("Back to start", key=f"back_{i}", on_click=reset_chat)


def render_thread():
    """Draw every message. Returns an empty slot where the loading bubble is shown."""
    messages = st.session_state.messages
    with st.container(key="thread"):
        for i, msg in enumerate(messages):
            if msg["role"] == "user":
                with st.container(key=f"bub_user_{i}"):
                    st.markdown(_plain(msg["text"]))
            else:
                _render_assistant(i, msg, is_last=(i == len(messages) - 1))
        return st.empty()


def _dock_suggestions() -> list[str]:
    messages = st.session_state.messages
    for msg in reversed(messages):
        if msg["role"] == "assistant" and not msg.get("error"):
            return msg.get("suggestions") or list(content.DEFAULT_SUGGESTIONS)
    return list(content.DEFAULT_SUGGESTIONS)


def render_dock() -> None:
    with st.container(key="dock"):
        with st.container(key="chips_dock"):
            for i, label in enumerate(_dock_suggestions()):
                st.button(label, key=f"chip_dock_{i}", on_click=queue_message, args=(label,))
        with st.container(key="composer_dock"):
            _composer("dock", content.COMPOSER_PLACEHOLDER_DOCK)
        st.html(cards.note_html("SIMULATION", content.DOCK_NOTE))


def scroll_to_latest() -> None:
    """Bring the newest message into view after the thread grows (Streamlit does not do this on its own)."""
    ss = st.session_state
    count = len(ss.messages)
    if count == ss.get("scrolled_to", 0):
        return
    ss.scrolled_to = count
    script = (
        "<script>/* " + str(count) + " */ (function () {"
        "const m = document.querySelector('[data-testid=\"stMain\"]');"
        "if (m) setTimeout(function () { m.scrollTo({ top: m.scrollHeight, behavior: 'smooth' }); }, 120);"
        "})();</script>"
    )
    with st.container(key="scroll_hook"):  # hidden by CSS; the count in the script makes each run unique
        st.html(script, unsafe_allow_javascript=True)


def process_pending(slot, agent: AgentClient) -> None:
    """Fetch the agent's reply for the queued request, showing a loading bubble while we wait."""
    ss = st.session_state
    pending = ss.pending
    if not pending:
        return
    with slot.container(key="turn_asst_loading"):
        with st.container(key="bub_asst_loading"):
            st.html(cards.loading_html(pending["kind"]))
    try:
        reply: AgentReply = (
            agent.application_status()
            if pending["kind"] == "lookup"
            else agent.send(pending["text"], verified=bool(ss.verified))
        )
    except Exception:  # noqa: BLE001 - any backend failure becomes the friendly error state
        ss.messages.append(
            {
                "role": "assistant",
                "text": "",
                "error": True,
                "reference": f"PW-{uuid.uuid4().hex[:4].upper()}",
                "retry": pending,
            }
        )
        ss.pending = None
        st.rerun()
        return
    ss.messages.append(
        {
            "role": "assistant",
            "text": reply.text,
            "cards": reply.cards,
            "action": reply.action,
            "suggestions": reply.suggestions,
        }
    )
    ss.awaiting = reply.action
    if reply.action:
        ss.dialog = reply.action
    ss.pending = None
    st.rerun()


# ---- Dialogs -------------------------------------------------------------------------------------------------------


@st.dialog("Verify it's you")
def _verify_dialog(agent: AgentClient) -> None:
    ss = st.session_state
    st.caption("Application status is private, so I need two details first.")
    with st.form("verify_form"):
        email = st.text_input("Email address", value=content.DEMO_EMAIL, key="verify_email")
        application_id = st.text_input("Application ID", value=content.DEMO_APPLICATION_ID, key="verify_app_id")
        st.caption("Your ID is in the confirmation email we sent when you applied. Used only to find your application.")
        submitted = st.form_submit_button("Verify and continue →", type="primary")
    if st.button("I can't find my ID", key="verify_no_id"):
        ss.awaiting = None
        queue_message(content.HUMAN_MESSAGE)
        st.rerun()
    if submitted:
        with st.spinner("Checking…"):
            result = agent.verify(email, application_id)
        if result.ok:
            ss.verified = {"name": result.name, "email": email.strip(), "application_id": application_id.strip()}
            ss.awaiting = None
            ss.pending = {"kind": "lookup"}
            st.rerun()
        else:
            st.error(result.message, icon=":material/error:")


@st.dialog("Talk to a person")
def _handoff_dialog(agent: AgentClient) -> None:
    ss = st.session_state
    st.caption("An advisor will follow up with you.")
    with st.form("handoff_form"):
        topic = st.selectbox("What's it about?", content.HANDOFF_TOPICS)
        best_time = st.selectbox("Best time to reach me", content.HANDOFF_TIMES)
        contact = st.radio("Contact me by", content.HANDOFF_CONTACT, horizontal=True)
        note = st.text_area(
            "Anything the advisor should know? (optional)",
            placeholder="For example: I need more time to find my diploma.",
        )
        st.caption("I'll share a summary of this chat so you don't have to repeat yourself.")
        submitted = st.form_submit_button("Send request →", type="primary")
    if submitted:
        with st.spinner("Sending…"):
            transcript = [{"role": m["role"], "text": m.get("text", "")} for m in ss.messages]
            result = agent.request_handoff(topic, best_time, contact, note, transcript)
        ss.messages.append(
            {
                "role": "assistant",
                "text": "Done. Your request is in, and I've passed along a summary of our chat.",
                "cards": [{"kind": "handoff_sent", "data": {"reference": result.reference, "message": result.message}}],
                "action": None,
                "suggestions": ["Explore programs", "Check my application"],
            }
        )
        ss.awaiting = None
        st.rerun()


def open_requested_dialog(agent: AgentClient) -> None:
    """Open the verify or handoff dialog once, on the run right after it was requested."""
    name = st.session_state.pop("dialog", None)
    if name == "verify":
        _verify_dialog(agent)
    elif name == "handoff":
        _handoff_dialog(agent)
