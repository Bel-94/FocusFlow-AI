"""FocusFlow AI — Streamlit home page.

Turns a daily brain dump into a prioritized action plan via Amazon Bedrock.
"""

from __future__ import annotations

import streamlit as st

from api_client import ApiError, generate_plan, get_api_base_url
from styles import inject_styles, render_brand, render_list_panel, render_text_panel

EXAMPLE_TASKS = """- Finish AWS article
- Study Terraform
- Prepare mentorship session
- Grocery shopping"""


def main() -> None:
    st.set_page_config(
        page_title="FocusFlow AI",
        page_icon="◉",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    inject_styles()
    render_brand(
        "An AI-powered productivity planner that turns your daily brain dump "
        "into a prioritized action plan."
    )

    if not get_api_base_url():
        st.warning(
            "API_BASE_URL is not set. Add it to the environment or "
            "`.streamlit/secrets.toml` before generating a plan."
        )

    tasks = st.text_area(
        "Today's brain dump",
        value=st.session_state.get("tasks_draft", EXAMPLE_TASKS),
        height=220,
        placeholder="List everything on your mind for today…",
        label_visibility="visible",
    )
    st.session_state["tasks_draft"] = tasks

    generate = st.button("Generate Plan", type="primary", use_container_width=False)

    if generate:
        if not tasks.strip():
            st.error("Add at least one task before generating a plan.")
        else:
            with st.spinner("Shaping your focus plan with Amazon Bedrock…"):
                try:
                    plan = generate_plan(tasks)
                    st.session_state["latest_plan"] = plan
                except ApiError as exc:
                    st.session_state.pop("latest_plan", None)
                    detail = f" (HTTP {exc.status_code})" if exc.status_code else ""
                    st.error(f"{exc}{detail}")

    plan = st.session_state.get("latest_plan")
    if plan:
        _render_plan(plan)


def _render_plan(plan: dict) -> None:
    st.markdown("### Your plan")

    if plan.get("warning"):
        st.warning(str(plan["warning"]))

    priority = plan.get("priority") or []
    schedule = plan.get("schedule") or []
    focus_tip = plan.get("focus_tip") or ""
    motivation = plan.get("motivation") or ""

    render_list_panel("Priority", [str(item) for item in priority], ordered=True)
    render_list_panel("Schedule", [str(item) for item in schedule], ordered=True)
    render_text_panel("Focus tip", str(focus_tip))
    render_text_panel("Motivation", str(motivation))

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
