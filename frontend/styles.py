"""Shared Streamlit styling for FocusFlow AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
  font-family: "Plus Jakarta Sans", sans-serif;
}

.stApp {
  background:
    radial-gradient(ellipse 900px 420px at 0% 0%, rgba(15, 118, 110, 0.14), transparent 60%),
    radial-gradient(ellipse 700px 380px at 100% 8%, rgba(14, 116, 144, 0.12), transparent 55%),
    linear-gradient(165deg, #f7faf9 0%, #eef3f5 48%, #e7eef1 100%);
  color: #132028;
}

[data-testid="stSidebar"] {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(19, 32, 40, 0.06);
}

.block-container {
  padding-top: 1.75rem;
  padding-bottom: 4.5rem;
  max-width: 880px;
}

.ff-hero {
  margin: 0.4rem 0 1.6rem 0;
  animation: ff-rise 0.65s ease-out both;
}

.ff-kicker {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #0f766e;
  margin-bottom: 0.55rem;
}

.ff-brand {
  font-family: "Fraunces", Georgia, serif;
  font-weight: 700;
  font-size: clamp(2.55rem, 7vw, 3.85rem);
  letter-spacing: -0.035em;
  line-height: 0.98;
  color: #102028;
  margin: 0 0 0.7rem 0;
}

.ff-tagline {
  font-size: 1.08rem;
  line-height: 1.55;
  color: #445560;
  max-width: 34rem;
  margin: 0;
}

.ff-composer {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(16, 32, 40, 0.08);
  border-radius: 22px;
  padding: 1.15rem 1.2rem 1.05rem;
  margin: 0.35rem 0 1.1rem;
  box-shadow: 0 18px 40px rgba(16, 40, 48, 0.05);
  animation: ff-rise 0.7s ease-out 0.05s both;
}

.ff-composer-label {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.15rem;
  font-weight: 600;
  color: #102028;
  margin: 0 0 0.2rem 0;
}

.ff-composer-hint {
  font-size: 0.9rem;
  color: #667788;
  margin: 0 0 0.85rem 0;
}

div[data-testid="stTextArea"] textarea {
  background: #f4f8f8 !important;
  border: 1px solid rgba(15, 118, 110, 0.18) !important;
  border-radius: 14px !important;
  color: #132028 !important;
  font-size: 1rem !important;
  line-height: 1.5 !important;
  min-height: 200px !important;
}

div[data-testid="stTextArea"] textarea:focus {
  border-color: #0f766e !important;
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.15) !important;
}

.ff-results-title {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.55rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #102028;
  margin: 1.4rem 0 0.35rem 0;
  animation: ff-rise 0.5s ease-out both;
}

.ff-results-sub {
  color: #5b6b78;
  font-size: 0.95rem;
  margin: 0 0 0.9rem 0;
}

.ff-panel {
  background: rgba(255, 255, 255, 0.86);
  border: 1px solid rgba(20, 33, 43, 0.07);
  border-radius: 18px;
  padding: 1.15rem 1.25rem 1.2rem;
  margin: 0.7rem 0;
  animation: ff-rise 0.55s ease-out both;
  position: relative;
  overflow: hidden;
}

.ff-panel::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #0f766e, #0e7490);
}

.ff-panel.ff-accent-priority::before { background: linear-gradient(180deg, #0f766e, #115e59); }
.ff-panel.ff-accent-schedule::before { background: linear-gradient(180deg, #0e7490, #155e75); }
.ff-panel.ff-accent-tip::before { background: linear-gradient(180deg, #b45309, #c2410c); }
.ff-panel.ff-accent-motivation::before { background: linear-gradient(180deg, #be185d, #9d174d); }

.ff-panel h3 {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.08rem;
  letter-spacing: -0.015em;
  margin: 0 0 0.7rem 0;
  color: #102028;
}

.ff-panel ol {
  margin: 0;
  padding-left: 0;
  list-style: none;
  counter-reset: ff-item;
}

.ff-panel ol li {
  counter-increment: ff-item;
  position: relative;
  padding: 0.55rem 0.55rem 0.55rem 2.55rem;
  margin: 0.35rem 0;
  line-height: 1.45;
  background: #f4f8f8;
  border-radius: 12px;
  color: #132028;
}

.ff-panel ol li::before {
  content: counter(ff-item);
  position: absolute;
  left: 0.55rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.45rem;
  height: 1.45rem;
  border-radius: 999px;
  background: #0f766e;
  color: #fff;
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  line-height: 1.45rem;
}

.ff-quote {
  font-size: 1.05rem;
  line-height: 1.55;
  color: #243542;
  margin: 0;
}

.ff-meta {
  font-size: 0.82rem;
  color: #6b7c88;
  margin: 0.55rem 0 0;
}

div.stButton > button[kind="primary"],
div.stButton > button {
  background: linear-gradient(135deg, #0f766e, #0e7490) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.01em;
  padding: 0.7rem 1.35rem !important;
  transition: transform 0.18s ease, filter 0.18s ease !important;
  box-shadow: 0 10px 24px rgba(15, 118, 110, 0.22);
}

div.stButton > button:hover {
  filter: brightness(1.05);
  transform: translateY(-1px);
  color: #fff !important;
}

div.stButton > button:focus {
  box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.2) !important;
}

@keyframes ff-rise {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .ff-brand { font-size: 2.35rem; }
  .ff-composer { padding: 1rem; }
}
"""


def inject_styles() -> None:
    """Inject brand fonts and page atmosphere."""
    st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)


def render_brand(tagline: str, kicker: str = "Amazon Bedrock · Nova Lite") -> None:
    """Render the hero brand lockup."""
    st.markdown(
        f"""
        <div class="ff-hero">
          <div class="ff-kicker">{_escape(kicker)}</div>
          <p class="ff-brand">FocusFlow AI</p>
          <p class="ff-tagline">{_escape(tagline)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_composer_header() -> None:
    """Render the composer section header above the text area."""
    st.markdown(
        """
        <div class="ff-composer">
          <p class="ff-composer-label">Today's brain dump</p>
          <p class="ff-composer-hint">Dump everything on your mind. We'll prioritize, schedule, and coach you.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_list_panel(
    title: str,
    items: list[str],
    *,
    ordered: bool = True,
    accent: str = "priority",
) -> None:
    """Render a titled list panel."""
    if not items:
        return
    tag = "ol" if ordered else "ul"
    rows = "".join(f"<li>{_escape(item)}</li>" for item in items)
    st.markdown(
        f'<div class="ff-panel ff-accent-{_escape(accent)}">'
        f"<h3>{_escape(title)}</h3><{tag}>{rows}</{tag}></div>",
        unsafe_allow_html=True,
    )


def render_text_panel(title: str, body: str, *, accent: str = "tip") -> None:
    """Render a titled text panel."""
    if not body:
        return
    st.markdown(
        f'<div class="ff-panel ff-accent-{_escape(accent)}"><h3>{_escape(title)}</h3>'
        f'<p class="ff-quote">{_escape(body)}</p></div>',
        unsafe_allow_html=True,
    )


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
