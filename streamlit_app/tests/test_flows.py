"""End-to-end journeys driven headlessly with Streamlit's AppTest."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from pathways import content

APP = str(Path(__file__).resolve().parents[1] / "streamlit_app.py")


@pytest.fixture
def at() -> AppTest:
    app = AppTest.from_file(APP, default_timeout=30)
    app.run()
    assert not app.exception
    return app


def _click(app: AppTest, key: str) -> None:
    app.button(key=key).click().run()
    assert not app.exception


def _submit_dialog(app: AppTest, name: str, label_prefix: str) -> None:
    """Click a button inside a dialog.

    In a browser, a dialog reruns only itself. AppTest reruns the whole script, where the one-shot
    ``dialog`` flag has already been consumed, so we re-arm it to keep the dialog open for the click.
    """
    app.session_state["dialog"] = name
    [b for b in app.button if b.label.startswith(label_prefix)][0].click().run()
    assert not app.exception


def test_home_shows_three_tiles_and_no_chat(at):
    assert at.session_state.messages == []
    for key in ("tile_explore", "tile_status", "tile_human"):
        assert at.button(key=key) is not None


def test_explore_tile_sends_one_canned_message(at):
    _click(at, "tile_explore")
    msgs = at.session_state.messages
    assert msgs[0] == {"role": "user", "text": content.EXPLORE_MESSAGE}
    assert msgs[1]["role"] == "assistant"
    assert {c["kind"] for c in msgs[1]["cards"]} >= {"program", "sources"}
    assert at.session_state.pending is None


def test_typed_message_goes_through_the_dock(at):
    _click(at, "tile_explore")
    at.text_input(key="msg_dock").set_value("How much does it cost?")
    send = [b for b in at.button if b.proto.form_id == "form_dock"]
    assert send, "dock composer has a send button"
    send[0].click().run()
    assert not at.exception
    users = [m["text"] for m in at.session_state.messages if m["role"] == "user"]
    assert users[-1] == "How much does it cost?"


def test_status_journey_verify_then_status(at):
    _click(at, "tile_status")
    # first run queues the message, the next run asks for verification
    assert at.session_state.messages[0]["text"] == content.STATUS_MESSAGE
    assert at.session_state.messages[-1]["action"] == "verify"
    assert at.session_state.verified is None

    # the dialog form is prefilled with the demo values; submit it
    assert [b for b in at.button if b.label.startswith("Verify and continue")], "verify dialog is open"
    _submit_dialog(at, "verify", "Verify and continue")
    assert at.session_state.verified["name"] == content.DEMO_NAME
    last = at.session_state.messages[-1]
    assert last["cards"][0]["kind"] == "status"
    assert last["cards"][0]["data"]["next_step"] == content.DEMO_NEXT_STEP


def test_wrong_credentials_keep_the_dialog_and_show_an_error(at):
    _click(at, "tile_status")
    at.text_input(key="verify_email").set_value("nobody@example.com")
    at.text_input(key="verify_app_id").set_value("APP-99999")
    _submit_dialog(at, "verify", "Verify and continue")
    assert at.session_state.verified is None
    assert len(at.error) == 1


def test_human_journey_ends_with_a_reference(at):
    _click(at, "tile_human")
    assert at.session_state.messages[-1]["action"] == "handoff"
    _submit_dialog(at, "handoff", "Send request")
    last = at.session_state.messages[-1]
    assert last["cards"][0]["kind"] == "handoff_sent"
    assert last["cards"][0]["data"]["reference"] == content.DEMO_HANDOFF_REFERENCE


def test_backend_failure_shows_a_recoverable_error(at):
    at.text_input(key="msg_home").set_value("simulate error")
    [b for b in at.button if b.proto.form_id == "form_home"][0].click().run()
    err = at.session_state.messages[-1]
    assert err.get("error") is True
    assert err["reference"].startswith("PW-")
    assert at.button(key="retry_1") is not None


def test_new_chat_resets_everything(at):
    _click(at, "tile_explore")
    assert at.session_state.messages
    _click(at, "new_chat")
    assert at.session_state.messages == []
    assert at.session_state.verified is None
    assert at.session_state.awaiting is None
