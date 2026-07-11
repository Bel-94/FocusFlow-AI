"""Shared Streamlit styling for FocusFlow AI."""

from __future__ import annotations

import streamlit as st

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Syne:wght@600;700;800&display=swap');

html, body, [class*="css"] {
  font-family: "Manrope", sans-serif;
}

.stApp {
  background:
    radial-gradient(1200px 600px at 10% -10%, #d7ebe7 0%, transparent 55%),
    radial-gradient(900px 500px at 100% 0%, #d9e4f0 0%, transparent 50%),
    linear-gradient(180deg, #f3f6f8 0%, #e8eef3 100%);
}

.block-container {
  padding-top: 2.5rem;
  padding-bottom: 4rem;
  max-width: 820px;
}

.ff-brand {
  font-family: "Syne", sans-serif;
  font-weight: 800;
  font-size: clamp(2.4rem, 6vw, 3.6rem);
  letter-spacing: -0.03em;
  line-height: 1.05;
  color: #14212b;
  margin: 0 0 0.6rem 0;
  animation: ff-rise 0.7s ease-out both;
}

.ff-tagline {
  font-size: 1.05rem;
  line-height: 1.55;
  color: #3b4a57;
  max-width: 36rem;
  margin: 0 0 1.75rem 0;
  animation: ff-rise 0.7s ease-out 0.08s both;
}

.ff-panel {
  background: rgba(255, 255, 255, 0.55);
  border: 1px solid rgba(20, 33, 43, 0.08);
  border-radius: 18px;
  padding: 1.15rem 1.25rem;
  margin: 0.85rem 0;
  backdrop-filter: blur(6px);
  animation: ff-rise 0.55s ease-out both;
}

.ff-panel h3 {
  font-family: "Syne", sans-serif;
  font-size: 1.05rem;
  letter-spacing: -0.02em;
  margin: 0 0 0.65rem 0;
  color: #0f766e;
}

.ff-panel ol, .ff-panel ul {
  margin: 0;
  padding-left: 1.15rem;
  color: #14212b;
}

.ff-panel li {
  margin: 0.35rem 0;
  line-height: 1.45;
}

.ff-quote {
  font-size: 1.02rem;
  line-height: 1.55;
  color: #243542;
  margin: 0;
}

.ff-meta {
  font-size: 0.85rem;
  color: #5b6b78;
  margin-top: 0.35rem;
}

div.stButton > button {
  background: #0f766e;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  transition: transform 0.18s ease, background 0.18s ease;
}

div.stButton > button:hover {
  background: #0b5f59;
  color: #fff;
  transform: translateY(-1px);
}

@keyframes ff-rise {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
"""


def inject_styles() -> None:
    """Inject brand fonts and page atmosphere."""
    st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)


def render_brand(tagline: str) -> None:
    """Render the hero brand lockup."""
    st.markdown('<p class="ff-brand">FocusFlow AI</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="ff-tagline">{tagline}</p>', unsafe_allow_html=True)


def render_list_panel(title: str, items: list[str], ordered: bool = True) -> None:
    """Render a titled list panel."""
    if not items:
        return
    tag = "ol" if ordered else "ul"
    rows = "".join(f"<li>{_escape(item)}</li>" for item in items)
    st.markdown(
        f'<div class="ff-panel"><h3>{_escape(title)}</h3><{tag}>{rows}</{tag}></div>',
        unsafe_allow_html=True,
    )


def render_text_panel(title: str, body: str) -> None:
    """Render a titled text panel."""
    if not body:
        return
    st.markdown(
        f'<div class="ff-panel"><h3>{_escape(title)}</h3>'
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
