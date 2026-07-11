"""FocusFlow AI — Streamlit home page.

Turns a daily brain dump into a prioritized action plan via Amazon Bedrock.
"""

from __future__ import annotations

import streamlit as st

from api_client import ApiError, generate_plan, get_api_base_url
from styles import (
    inject_styles,
    render_brand,
    render_list_panel,
    render_text_panel,
)

EXAMPLE_TASKS = """- Finish AWS article
- Study Terraform
- Prepare mentorship session
- Grocery shopping"""


def _init_state() -> None:
    if "latest_plan" not in st.session_state:
        st.session_state.latest_plan = None
    # Apply deferred textarea updates BEFORE the widget with key="tasks_draft" exists.
    pending = st.session_state.pop("_pending_tasks_draft", None)
    if pending is not None:
        st.session_state.tasks_draft = pending
    elif "tasks_draft" not in st.session_state:
        st.session_state.tasks_draft = EXAMPLE_TASKS


def main() -> None:
    st.set_page_config(
        page_title="FocusFlow AI",
        page_icon="◉",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    _init_state()
    inject_styles()
    render_brand(
        "Turn a messy day into a clear plan; priorities, focus blocks, "
        "and coaching powered by Amazon Bedrock."
    )

    if not get_api_base_url():
        st.warning(
            "API_BASE_URL is not set. Add it to the environment or "
            "`.streamlit/secrets.toml` before generating a plan."
        )

    st.markdown(
        '<p class="ff-composer-label">Today\'s brain dump</p>'
        '<p class="ff-composer-hint">List everything on your mind. '
        "After you generate a plan, this box clears so you can start fresh.</p>",
        unsafe_allow_html=True,
    )

    tasks = st.text_area(
        "Today's brain dump",
        height=220,
        placeholder="e.g.\n- Ship the Lambda deploy\n- Prep mentorship notes\n- Buy groceries",
        label_visibility="collapsed",
        key="tasks_draft",
    )

    col_generate, col_example, _ = st.columns([1.2, 1, 2])
    with col_generate:
        generate = st.button("Generate Plan", type="primary", use_container_width=True)
    with col_example:
        load_example = st.button("Load example", use_container_width=True)

    if load_example:
        # Defer mutation until the next run (before the widget is created).
        st.session_state._pending_tasks_draft = EXAMPLE_TASKS
        st.rerun()

    if generate:
        if not str(tasks).strip():
            st.error("Add at least one task before generating a plan.")
        else:
            with st.spinner("Shaping your focus plan with Amazon Bedrock…"):
                try:
                    plan = generate_plan(str(tasks))
                    st.session_state.latest_plan = plan
                    # Clear on the next run so Streamlit allows the widget key update.
                    st.session_state._pending_tasks_draft = ""
                    st.rerun()
                except ApiError as exc:
                    st.session_state.latest_plan = None
                    detail = f" (HTTP {exc.status_code})" if getattr(exc, "status_code", None) else ""
                    st.error(f"{exc}{detail}")

    plan = st.session_state.get("latest_plan")
    if plan:
        _render_plan(plan)


def _render_plan(plan: dict) -> None:
    st.markdown('<p class="ff-results-title">Your plan</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="ff-results-sub">Prioritized and scheduled from your last brain dump.</p>',
        unsafe_allow_html=True,
    )

    if plan.get("warning"):
        st.warning(str(plan["warning"]))

    priority = plan.get("priority") or []
    schedule = plan.get("schedule") or []
    focus_tip = plan.get("focus_tip") or ""
    motivation = plan.get("motivation") or ""

    render_list_panel("Priority", [str(item) for item in priority], ordered=True, accent="priority")
    render_list_panel("Schedule", [str(item) for item in schedule], ordered=True, accent="schedule")

    tip_col, motivation_col = st.columns(2)
    with tip_col:
        render_text_panel("Focus tip", str(focus_tip), accent="tip")
    with motivation_col:
        render_text_panel("Motivation", str(motivation), accent="motivation")

    meta_bits: list[str] = []
    if plan.get("planId"):
        meta_bits.append(f"Plan ID: {plan['planId']}")
    if plan.get("createdAt"):
        meta_bits.append(f"Saved: {plan['createdAt']}")
    if meta_bits:
        st.markdown(
            f'<p class="ff-meta">{" · ".join(meta_bits)}</p>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
