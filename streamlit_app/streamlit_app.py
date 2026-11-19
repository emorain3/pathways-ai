"""Pathways AI: entry point. Run locally with `streamlit run streamlit_app.py`."""

import streamlit as st

from pathways import ui

st.set_page_config(
    page_title="Pathways AI (simulation)",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

ui.init_state()
ui.inject_theme()
agent = ui.get_cached_agent()

in_chat = bool(st.session_state.messages)
ui.render_header(in_chat)

if in_chat:
    loading_slot = ui.render_thread()
    ui.render_dock()
    ui.scroll_to_latest()
    ui.process_pending(loading_slot, agent)
else:
    ui.render_home()

ui.open_requested_dialog(agent)
