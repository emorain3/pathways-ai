"""HTML builders for the rich cards inside the conversation. Every dynamic value is escaped."""

from __future__ import annotations

from html import escape as esc

from . import theme

_CHECK_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='#FFFFFF' stroke-width='3' "
    "stroke-linecap='round' stroke-linejoin='round'><path d='M5 12l4.5 4.5L19 7'/></svg>"
)
_DOC_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='#262552' stroke-width='2.2' "
    "stroke-linecap='round' stroke-linejoin='round'><path d='M6 3h8l5 5v13H6z'/><path d='M14 3v5h5'/></svg>"
)
_CHECK = theme.svg_img(_CHECK_SVG, 17, 17)
_CHECK_BIG = theme.svg_img(_CHECK_SVG, 30, 30)
_DOC = theme.svg_img(_DOC_SVG, 14, 14)


def program_card(data: dict) -> str:
    pills = "".join(f'<span class="pw-pill">{esc(c)}</span>' for c in data["chips"])
    return (
        '<div class="pw-card pw-program"><span class="pw-mono">PROGRAM</span>'
        f'<h3>{esc(data["name"])}</h3><div class="pw-chiprow">{pills}</div></div>'
    )


def sources_card(data: dict) -> str:
    links = "".join(
        f'<a class="pw-src" href="{esc(s["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{_DOC}{esc(s["title"])}</a>'
        for s in data["items"]
    )
    return f'<div class="pw-sources"><span class="pw-mono">SOURCES</span>{links}</div>'


def status_card(data: dict) -> str:
    steps = []
    for i, label in enumerate(data["stages"]):
        if i < data["current"]:
            state, node, hint = "done", _CHECK, " (completed)"
        elif i == data["current"]:
            state, node, hint = "current", str(i + 1), " (current step)"
        else:
            state, node, hint = "todo", str(i + 1), ""
        current = ' aria-current="step"' if state == "current" else ""
        steps.append(
            f'<li class="pw-step {state}"{current}><span class="pw-node">{node}</span>'
            f'<span class="pw-step-label">{esc(label)}<span class="pw-vh">{hint}</span></span></li>'
        )
    nxt = data["next_step"]
    return (
        '<div class="pw-card pw-status">'
        f'<div class="pw-status-head"><h3>{esc(data["program"])}</h3><span class="pw-mono">{esc(data["application_id"])}</span></div>'
        f'<ol class="pw-track" aria-label="Application progress">{"".join(steps)}</ol>'
        '<div class="pw-next"><span class="pw-mono">NEXT STEP</span>'
        f'<p class="big">{esc(nxt["headline"])}</p><p class="small">{esc(nxt["detail"])}</p>'
        f'<div><a class="pw-btn" href="{esc(nxt["link_url"], quote=True)}" target="_blank" rel="noopener noreferrer">'
        f'{esc(nxt["link_label"])} ↗</a></div></div></div>'
    )


def handoff_sent_card(data: dict) -> str:
    return (
        '<div class="pw-card pw-sent" role="status"><span class="orb">' + _CHECK_BIG + "</span>"
        '<div class="body"><span class="pw-mono">REQUEST SENT</span>'
        '<span class="head">An advisor will follow up.</span>'
        f'<span class="sub">{esc(data["message"])}</span></div>'
        f'<div class="pw-ref"><span class="pw-mono">REFERENCE</span><b>{esc(data["reference"])}</b></div></div>'
    )


RENDERERS = {
    "program": program_card,
    "sources": sources_card,
    "status": status_card,
    "handoff_sent": handoff_sent_card,
}


def render_card(card: dict) -> str:
    renderer = RENDERERS.get(card["kind"])
    return renderer(card["data"]) if renderer else ""


def brand_html() -> str:
    return (
        '<div class="pw-brand"><div class="pw-logo">'
        + theme.cloud_svg("hd", 54, 41, "pw-float")
        + theme.sparkle_svg("hd", 24, "pw-sparkle pw-twinkle")
        + '<span class="pw-word">Pathways AI</span></div>'
        '<span class="pw-tag"><i></i>SIMULATED DEMO</span></div>'
    )


def hero_html(title: str, paragraphs: list[str]) -> str:
    return (
        '<div class="pw-hero"><div class="pw-mascot"><div class="pw-halo" aria-hidden="true"></div>'
        + theme.cloud_svg("hero", 128, 98, "pw-float")
        + theme.sparkle_svg("hero1", 40, "s1 pw-twinkle")
        + theme.sparkle_svg("hero2", 20, "s2 pw-twinkle")
        + f'</div><h1 class="pw-title">{esc(title)}</h1>'
        + "".join(f'<p class="pw-lede">{esc(text)}</p>' for text in paragraphs)
        + "</div>"
    )


def loading_html(kind: str) -> str:
    if kind == "lookup":
        return (
            '<div class="pw-loading" role="status"><div class="row"><span class="pw-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
            "<span>Looking up your application…</span></div>"
            '<div aria-hidden="true"><span class="pw-shim" style="width:92%"></span><span class="pw-shim" style="width:74%"></span>'
            '<span class="pw-shim" style="width:48%"></span></div>'
            '<div class="pw-steps"><span>✓ Identity confirmed</span><span>● Checking your application record</span>'
            "<span>○ Finding your next step</span></div></div>"
        )
    return (
        '<div class="pw-loading" role="status"><div class="row"><span class="pw-dots" aria-hidden="true"><i></i><i></i><i></i></span>'
        "<span>One moment…</span></div></div>"
    )


def error_html(reference: str) -> str:
    return (
        '<div class="pw-err" role="alert"><span class="bang" aria-hidden="true">!</span><div>'
        '<span class="t">That didn\'t go through.</span>'
        "<span class=\"d\">I couldn't reach the application system just now. Nothing on your account was changed.</span>"
        f'<span class="ref pw-mono">REF {esc(reference)}</span></div></div>'
    )


def note_html(label: str, text: str) -> str:
    return f'<p class="pw-note"><span class="pw-pill">{esc(label)}</span><span>{esc(text)}</span></p>'
