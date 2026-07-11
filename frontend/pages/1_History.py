"""History page — previous FocusFlow AI plans from DynamoDB."""

from __future__ import annotations

import streamlit as st

from api_client import ApiError, fetch_history, get_api_base_url
from styles import inject_styles, render_brand, render_list_panel, render_text_panel

st.set_page_config(
    page_title="History · FocusFlow AI",
    page_icon="◉",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_styles()
render_brand(
    "Revisit plans you generated earlier — newest first.",
    kicker="Saved plans · DynamoDB",
)

if not get_api_base_url():
    st.warning(
        "API_BASE_URL is not set. Add it to the environment or "
        "`.streamlit/secrets.toml` to load history."
    )
    st.stop()

col_refresh, _ = st.columns([1, 3])
with col_refresh:
    refresh = st.button("Refresh", use_container_width=True)

if refresh or "history_plans" not in st.session_state:
    with st.spinner("Loading history…"):
        try:
            st.session_state["history_plans"] = fetch_history()
            st.session_state.pop("history_error", None)
        except ApiError as exc:
            st.session_state["history_plans"] = []
            st.session_state["history_error"] = str(exc)

if st.session_state.get("history_error"):
    st.error(st.session_state["history_error"])

plans = st.session_state.get("history_plans") or []

if not plans and not st.session_state.get("history_error"):
    st.info("No plans yet. Generate one from the home page.")
else:
    for index, plan in enumerate(plans):
        created = plan.get("createdAt") or "Unknown time"
        plan_id = plan.get("planId") or f"plan-{index}"
        label = f"{created} · {plan_id[:8]}"

        with st.expander(label, expanded=(index == 0)):
            tasks = str(plan.get("tasks") or "").strip()
            if tasks:
                st.markdown("**Original brain dump**")
                st.code(tasks, language=None)

            render_list_panel(
                "Priority",
                [str(item) for item in (plan.get("priority") or [])],
                ordered=True,
                accent="priority",
            )
            render_list_panel(
                "Schedule",
                [str(item) for item in (plan.get("schedule") or [])],
                ordered=True,
                accent="schedule",
            )
            tip_col, motivation_col = st.columns(2)
            with tip_col:
                render_text_panel(
                    "Focus tip",
                    str(plan.get("focus_tip") or ""),
                    accent="tip",
                )
            with motivation_col:
                render_text_panel(
                    "Motivation",
                    str(plan.get("motivation") or ""),
                    accent="motivation",
                )
