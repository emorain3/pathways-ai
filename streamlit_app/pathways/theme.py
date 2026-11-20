"""Visual layer: the aurora-glass look from Concept F, as one injected stylesheet.

Streamlit gives every ``st.container(key="x")`` the class ``st-key-x``, and every keyed widget the same,
so the layout code stays plain Streamlit and this file does all the styling through those hooks.
"""

from __future__ import annotations

import base64
from urllib.parse import quote

from . import content

INK = "#262552"
SECONDARY = "#3B3B6B"


def svg_uri(svg: str) -> str:
    """Inline an SVG string as a CSS ``url(...)`` value."""
    return 'url("data:image/svg+xml;utf8,' + quote(svg, safe="/:=;,'() ") + '")'


def css_string(text: str) -> str:
    """Escape text for use inside a CSS ``content: "..."`` declaration."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


# ---- SVG pieces ---------------------------------------------------------------------------------------------
CLOUD_PATH = "M9 23h16a7 7 0 0 0 1.2-13.9A9 9 0 0 0 9.2 8.6 7.2 7.2 0 0 0 9 23z"
SPARKLE_PATH = "M22 2Q24 18 42 22Q24 26 22 42Q20 26 2 22Q20 18 22 2Z"


def svg_img(svg: str, width: int, height: int, css_class: str = "") -> str:
    """An SVG as a base64 ``<img>``.

    ``st.html`` sanitizes markup and drops inline ``<svg>``, but keeps ``<img>`` with a data URI, so every
    inline illustration in the app goes through here.
    """
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return (
        f'<img class="{css_class}" width="{width}" height="{height}" alt="" aria-hidden="true" '
        f'src="data:image/svg+xml;base64,{data}">'
    )


def cloud_svg(uid: str, width: int, height: int, css_class: str = "") -> str:
    """The glass cloud mascot (``uid`` is kept for API symmetry; each image is self-contained)."""
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 34 26'><defs>"
        "<linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
        "<stop offset='0' stop-color='#FFFFFF' stop-opacity='.98'/>"
        "<stop offset='.55' stop-color='#D4E8FF' stop-opacity='.92'/>"
        "<stop offset='1' stop-color='#FFCFE6' stop-opacity='.92'/></linearGradient></defs>"
        f"<path d='{CLOUD_PATH}' fill='url(#g)' stroke='#FFFFFF' stroke-width='1.1' stroke-linejoin='round'/>"
        "<path d='M12 11.5a6 6 0 0 1 6-3.4' fill='none' stroke='#FFFFFF' stroke-width='1.2' stroke-linecap='round'/>"
        f"<circle cx='13.5' cy='15' r='1.6' fill='{INK}'/><circle cx='21.5' cy='15' r='1.6' fill='{INK}'/>"
        f"<path d='M14.7 18.4q2.3 2.4 4.6 0' fill='none' stroke='{INK}' stroke-width='1.4' stroke-linecap='round'/>"
        "<circle cx='11' cy='18' r='1.7' fill='#FF8FC0' opacity='.7'/>"
        "<circle cx='24' cy='18' r='1.7' fill='#FF8FC0' opacity='.7'/></svg>"
    )
    return svg_img(svg, width, height, css_class)


def sparkle_svg(uid: str, size: int, css_class: str = "") -> str:
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 44 44'><defs>"
        "<linearGradient id='s' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#FF8FC0'/>"
        "<stop offset='1' stop-color='#7FB2FF'/></linearGradient></defs>"
        f"<path d='{SPARKLE_PATH}' fill='url(#s)'/></svg>"
    )
    return svg_img(svg, size, size, css_class)


_AVATAR = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='46' height='46' viewBox='0 0 46 46'>"
    "<defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#fff'/>"
    "<stop offset='.55' stop-color='#D4E8FF'/><stop offset='1' stop-color='#FFCFE6'/></linearGradient></defs>"
    "<circle cx='23' cy='23' r='22' fill='#fff' fill-opacity='.62' stroke='#fff' stroke-width='1'/>"
    "<g transform='translate(8.4 11.8) scale(.86)'>"
    f"<path d='{CLOUD_PATH}' fill='url(#g)' stroke='#9AA7F5' stroke-width='1' stroke-linejoin='round'/>"
    f"<circle cx='13.5' cy='15' r='1.7' fill='{INK}'/><circle cx='21.5' cy='15' r='1.7' fill='{INK}'/>"
    f"<path d='M14.7 18.4q2.3 2.4 4.6 0' fill='none' stroke='{INK}' stroke-width='1.4' stroke-linecap='round'/>"
    "</g></svg>"
)

_ARROW = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='#fff' stroke-width='2.4' "
    "stroke-linecap='round' stroke-linejoin='round'><path d='M4 12h15M13 6l6 6-6 6'/></svg>"
)
_REFRESH = (
    f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{INK}' stroke-width='2.4' "
    "stroke-linecap='round' stroke-linejoin='round'><path d='M20 11a8 8 0 1 0-2.3 5.7'/><path d='M20 4v7h-7'/></svg>"
)
_GRAIN = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'>"
    "<feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/>"
    "<feColorMatrix values='0 0 0 0 .3 0 0 0 0 .3 0 0 0 0 .5 0 0 0 .55 0'/></filter>"
    "<rect width='180' height='180' filter='url(#n)'/></svg>"
)

FONT_IMPORT = (
    "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,600;1,700"
    "&family=Poppins:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');"
)

# ---- Static stylesheet (plain string: CSS braces must not be f-string escaped) --------------------------------
BASE_CSS = """
:root{
  --pw-ink:#262552; --pw-sec:#3B3B6B; --pw-violet:#5B57E8; --pw-violet2:#8A4FE0;
  --pw-grad:linear-gradient(135deg,#5B57E8,#8A4FE0);
  --pw-glass:rgba(255,255,255,.58);
  --pw-border:rgba(255,255,255,.85);
  --pw-shadow:0 14px 40px rgba(104,92,200,.16),inset 0 1px 0 rgba(255,255,255,.9);
}

/* ---------- page ---------- */
.stApp{
  isolation:isolate;
  font-family:'Poppins',sans-serif; color:var(--pw-ink);
  background:
    radial-gradient(60vmax 60vmax at -8% -10%, rgba(255,179,214,.85), transparent 60%),
    radial-gradient(65vmax 65vmax at 108% -12%, rgba(166,205,255,.9), transparent 60%),
    radial-gradient(75vmax 50vmax at 35% 112%, rgba(210,192,255,.8), transparent 62%),
    radial-gradient(40vmax 40vmax at 104% 78%, rgba(255,200,226,.7), transparent 62%),
    radial-gradient(40vmax 40vmax at -6% 82%, rgba(185,218,255,.75), transparent 62%),
    #EEF1FF;
  background-attachment:fixed;
}
.stApp::before{
  content:""; position:fixed; inset:0; z-index:-1; pointer-events:none;
  background-image:__GRAIN__; opacity:.12; mix-blend-mode:multiply;
}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer{display:none !important}
[data-testid="stMainBlockContainer"]{max-width:860px; padding:20px 28px 28px}
.stApp p, .stApp label, .stApp button, .stApp input, .stApp textarea, .stApp li{font-family:'Poppins',sans-serif}
.stApp :focus-visible{outline:3px solid var(--pw-ink) !important; outline-offset:3px !important}

.pw-vh{position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap}

/* ---------- header ---------- */
.st-key-head{flex-direction:row !important; flex-wrap:wrap; align-items:center !important; justify-content:space-between; gap:10px 20px !important}
.st-key-head > *{width:auto !important; flex:0 0 auto}
.st-key-head > .st-key-new_chat{margin-left:auto}
.pw-brand{display:flex; flex-wrap:wrap; align-items:center; gap:10px 18px}
.pw-logo{position:relative; display:flex; align-items:center; gap:14px}
.pw-logo .pw-sparkle{position:absolute; top:-2px; left:50px}
.pw-word{font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:700; font-size:38px; line-height:1; margin-left:12px; color:var(--pw-ink)}
.pw-tag{display:inline-flex; align-items:center; gap:8px; border-radius:999px; padding:4px 13px; background:rgba(255,255,255,.75);
  border:1px solid rgba(91,87,232,.28); font:12px/1.4 'Share Tech Mono',monospace; letter-spacing:.12em; color:var(--pw-ink)}
.pw-tag i{width:8px; height:8px; border-radius:50%; background:linear-gradient(135deg,#FF8FC0,#7FB2FF); display:block}
.pw-float{animation:pw-float 6s ease-in-out infinite; filter:drop-shadow(0 6px 12px rgba(104,92,200,.4))}
.pw-twinkle{animation:pw-twinkle 3.2s ease-in-out infinite; filter:drop-shadow(0 0 7px rgba(138,120,255,.7))}

/* ---------- home hero ---------- */
.pw-hero{display:flex; flex-direction:column; align-items:center; gap:22px; text-align:center; padding-top:6px}
.pw-mascot{position:relative; width:150px; height:124px; display:flex; align-items:center; justify-content:center}
.pw-halo{position:absolute; inset:-10px; border-radius:50%; filter:blur(6px);
  background:radial-gradient(circle,rgba(255,255,255,.95) 0,rgba(255,179,214,.55) 38%,rgba(166,205,255,.35) 62%,rgba(255,255,255,0) 72%)}
.pw-mascot .pw-float{position:relative; display:block; filter:drop-shadow(0 12px 22px rgba(104,92,200,.4))}
.pw-mascot .s1{position:absolute; top:-8px; right:-26px}
.pw-mascot .s2{position:absolute; top:44px; right:-44px; animation-delay:1.1s}
.pw-title{margin:0; padding:0; max-width:760px; font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:700;
  line-height:1.04; font-size:clamp(40px,5.8vw,62px); letter-spacing:0;
  background:linear-gradient(90deg,#4A46D8,#A93C9E); -webkit-background-clip:text; background-clip:text; color:transparent}
.pw-lede{margin:0; max-width:640px; font-size:17px; line-height:1.65; color:var(--pw-sec)}
.pw-lede + .pw-lede{margin-top:-12px}

/* ---------- buttons: chips ---------- */
.st-key-chips_home, .st-key-chips_dock{flex-direction:row !important; flex-wrap:wrap; gap:8px 10px !important}
.st-key-chips_home > *, .st-key-chips_dock > *{width:auto !important; flex:0 0 auto}
.st-key-chips_home button, .st-key-chips_dock button{
  min-height:44px; padding:0 18px; border-radius:999px; background:rgba(255,255,255,.55);
  border:1px solid rgba(91,87,232,.3); box-shadow:none; color:var(--pw-ink); transition:background .15s ease, transform .15s ease}
.st-key-chips_dock button{background:rgba(255,255,255,.62); border-color:rgba(255,255,255,.95); box-shadow:0 4px 14px rgba(104,92,200,.12)}
.st-key-chips_home button:hover, .st-key-chips_dock button:hover{background:#fff; transform:translateY(-1px); border-color:rgba(91,87,232,.45); color:var(--pw-ink)}
.st-key-chips_home button p, .st-key-chips_dock button p{font-size:13.5px; font-weight:500; color:var(--pw-ink); margin:0}

/* ---------- composer (home card and conversation dock) ---------- */
.st-key-composer_home{
  /* top padding = bottom padding + one pill row (44px) + gap (10px), which centres the input row in the card */
  border:2px solid transparent; border-radius:28px; padding:68px 16px 14px 24px; gap:10px !important;
  background:linear-gradient(rgba(255,255,255,.78),rgba(255,255,255,.78)) padding-box,
             linear-gradient(120deg,#FF8FC0,#8FBEFF,#B49BFF) border-box;
  box-shadow:0 20px 50px rgba(104,92,200,.22)}
.st-key-composer_dock{
  border-radius:999px; padding:6px 8px 6px 26px; background:var(--pw-glass); border:1px solid var(--pw-border);
  -webkit-backdrop-filter:blur(22px) saturate(160%); backdrop-filter:blur(22px) saturate(160%); box-shadow:var(--pw-shadow)}
[class*="st-key-composer_"] [data-testid="stForm"]{border:0 !important; padding:0 !important; background:transparent}
[class*="st-key-composer_"] [data-testid="stForm"] > [data-testid="stVerticalBlock"]{flex-direction:row !important; align-items:center !important; flex-wrap:nowrap; gap:10px !important}
[class*="st-key-composer_"] [data-testid="stForm"] > [data-testid="stVerticalBlock"] > *:first-child{flex:1 1 auto; min-width:0; width:auto !important}
[class*="st-key-composer_"] [data-testid="stForm"] > [data-testid="stVerticalBlock"] > *:last-child{flex:0 0 auto; width:auto !important}
[class*="st-key-composer_"] [data-testid="stTextInputRootElement"]{border:0 !important; background:transparent !important; box-shadow:none !important; min-height:48px}
[class*="st-key-composer_"] input{background:transparent !important; color:var(--pw-ink) !important; font-size:17px; padding-left:0 !important; text-overflow:ellipsis}
.st-key-composer_dock input{font-size:15px}
[class*="st-key-composer_"] input::placeholder{color:#4A4A7D !important; opacity:1 !important}
[class*="st-key-composer_"] [data-testid="InputInstructions"]{display:none}
[class*="st-key-composer_"] [data-testid="stBaseButton-primaryFormSubmit"]{
  width:52px; height:52px; min-height:52px; padding:0; border:0; border-radius:50%; background:var(--pw-grad) !important;
  box-shadow:0 10px 22px rgba(91,87,232,.42), inset 0 1px 0 rgba(255,255,255,.4); position:relative}
.st-key-composer_dock [data-testid="stBaseButton-primaryFormSubmit"]{width:48px; height:48px; min-height:48px}
.stApp [class*="st-key-composer_"] [data-testid="stBaseButton-primaryFormSubmit"] p{font-size:0 !important; line-height:0 !important; margin:0}
[class*="st-key-composer_"] [data-testid="stBaseButton-primaryFormSubmit"]::after{
  content:""; position:absolute; inset:0; background:__ARROW__ center/22px no-repeat}

/* ---------- start-over button ---------- */
.st-key-new_chat button{
  min-height:44px; padding:0 18px 0 40px; border-radius:999px; background:var(--pw-glass); border:1px solid var(--pw-border);
  box-shadow:var(--pw-shadow); color:var(--pw-ink); position:relative;
  -webkit-backdrop-filter:blur(16px) saturate(150%); backdrop-filter:blur(16px) saturate(150%)}
.st-key-new_chat button::before{content:""; position:absolute; left:16px; top:50%; width:16px; height:16px; margin-top:-8px; background:__REFRESH__ center/16px no-repeat}
.st-key-new_chat button p{font-size:13.5px; font-weight:500; margin:0}

/* ---------- conversation ---------- */
.st-key-thread{gap:20px !important; padding-top:6px}
[class*="st-key-bub_user_"]{width:fit-content; max-width:100%; margin-left:auto; padding:12px 18px; border-radius:20px 20px 6px 20px;
  background:var(--pw-grad); color:#fff; box-shadow:0 10px 24px rgba(91,87,232,.32)}
[class*="st-key-bub_user_"] p{color:#fff; font-size:15px; line-height:1.5; font-weight:500}
[class*="st-key-bub_"] [data-testid="stMarkdownContainer"]{margin-bottom:0 !important}
[class*="st-key-bub_"] [data-testid="stMarkdownContainer"] p{margin:0 !important}
[class*="st-key-bub_"] [data-testid="stMarkdownContainer"] p + p{margin-top:8px !important}
[data-testid="stLayoutWrapper"]:has(> [class*="st-key-bub_user_"]){align-self:flex-end; max-width:78%}
[class*="st-key-turn_asst_"]{position:relative; padding-left:60px; gap:14px !important}
[class*="st-key-turn_asst_"]::before{content:""; position:absolute; left:0; top:0; width:46px; height:46px; background:__AVATAR__ center/46px no-repeat;
  filter:drop-shadow(0 6px 14px rgba(104,92,200,.18))}
[class*="st-key-bub_asst_"]{padding:14px 18px; border-radius:20px 20px 20px 6px; background:var(--pw-glass); border:1px solid var(--pw-border);
  -webkit-backdrop-filter:blur(22px) saturate(160%); backdrop-filter:blur(22px) saturate(160%); box-shadow:var(--pw-shadow)}
[class*="st-key-bub_asst_"] p{font-size:15px; line-height:1.6; color:var(--pw-ink)}

[class*="st-key-bub_err_"]{padding:14px 18px; border-radius:20px 20px 20px 6px; background:rgba(255,228,238,.78); border:1px solid rgba(255,255,255,.9);
  -webkit-backdrop-filter:blur(22px); backdrop-filter:blur(22px); box-shadow:0 14px 40px rgba(200,70,120,.16), inset 0 1px 0 rgba(255,255,255,.9)}
.pw-err{display:flex; align-items:flex-start; gap:12px; color:var(--pw-ink)}
.pw-err .bang{flex:none; display:flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:#B3265F; color:#fff; font:700 16px/1 'Share Tech Mono',monospace}
.pw-err .t{display:block; font-weight:600; font-size:16px; margin-bottom:4px}
.pw-err .d{display:block; font-size:15px; line-height:1.55}
.pw-err .ref{display:block; margin-top:8px}

/* cards */
.pw-card{border-radius:22px; padding:18px 22px; background:var(--pw-glass); border:1px solid var(--pw-border); box-shadow:var(--pw-shadow);
  -webkit-backdrop-filter:blur(22px) saturate(160%); backdrop-filter:blur(22px) saturate(160%); color:var(--pw-ink)}
.pw-card h3{margin:0; padding:0; font-size:22px; line-height:1.2; font-weight:600; color:var(--pw-ink)}
.pw-mono{font:12px/1.4 'Share Tech Mono',monospace; letter-spacing:.14em; color:var(--pw-sec)}
.pw-program{display:flex; flex-direction:column; gap:12px; background:linear-gradient(135deg,rgba(255,255,255,.7),rgba(255,214,234,.55))}
.pw-chiprow{display:flex; flex-wrap:wrap; gap:8px}
.pw-pill{display:inline-flex; align-items:center; border-radius:999px; padding:4px 13px; background:rgba(255,255,255,.75);
  border:1px solid rgba(91,87,232,.28); font:12px/1.4 'Share Tech Mono',monospace; letter-spacing:.08em; color:var(--pw-ink)}
.pw-sources{display:flex; flex-wrap:wrap; align-items:center; gap:8px 10px}
.pw-src{display:inline-flex; align-items:center; gap:7px; min-height:44px; box-sizing:border-box; padding:0 16px; border-radius:999px;
  background:rgba(255,255,255,.62); border:1px solid rgba(91,87,232,.3); color:var(--pw-ink) !important; font-weight:500; font-size:13px; text-decoration:none !important}
.pw-src:hover{background:#fff}
.pw-btn{display:inline-flex; align-items:center; justify-content:center; gap:8px; min-height:48px; box-sizing:border-box; padding:0 24px; border-radius:999px;
  background:var(--pw-grad); color:#fff !important; font-weight:600; font-size:14px; text-decoration:none !important;
  box-shadow:0 10px 24px rgba(91,87,232,.38), inset 0 1px 0 rgba(255,255,255,.35)}

/* status card + progress track */
.pw-status{display:flex; flex-direction:column; gap:20px; border-radius:24px; padding:20px 24px 24px}
.pw-status-head{display:flex; flex-wrap:wrap; align-items:baseline; justify-content:space-between; gap:4px 16px}
.stHtml ol.pw-track, ol.pw-track{list-style:none; margin:0 !important; padding:0 !important; display:flex; align-items:flex-start; width:100%}
ol.pw-track > li{margin:0 !important; padding:0 !important}
.pw-step{position:relative; flex:1 1 0; min-width:0; display:flex; flex-direction:column; align-items:center; gap:8px; text-align:center}
.pw-step + .pw-step::before{content:""; position:absolute; top:15px; right:50%; width:100%; height:6px; border-radius:3px; background:rgba(91,87,232,.16)}
.pw-step.done + .pw-step::before, .pw-step.current::before{background:linear-gradient(90deg,#5B57E8,#C0408A); box-shadow:0 0 14px rgba(138,79,224,.55)}
.pw-step.done + .pw-step.todo::before{background:linear-gradient(90deg,#5B57E8,#C0408A)}
.pw-node{position:relative; z-index:1; width:36px; height:36px; box-sizing:border-box; display:flex; align-items:center; justify-content:center; border-radius:50%;
  font:15px/1 'Share Tech Mono',monospace; color:var(--pw-sec); background:rgba(255,255,255,.7); border:1.5px solid #6F6CCB}
.pw-step.done .pw-node{background:var(--pw-grad); border:0; box-shadow:0 6px 16px rgba(91,87,232,.4)}
.pw-step.current .pw-node{background:#fff; border:3px solid #8A4FE0; color:#4A46D8; font-weight:700;
  box-shadow:0 0 0 6px rgba(138,79,224,.16), 0 0 20px rgba(138,79,224,.5)}
.pw-step-label{font-size:13px; font-weight:400; color:var(--pw-sec)}
.pw-step.done .pw-step-label{color:var(--pw-ink); font-weight:500}
.pw-step.current .pw-step-label{color:var(--pw-ink); font-weight:700}
.pw-next{display:flex; flex-direction:column; gap:8px; border-radius:18px; padding:16px 20px; border:1px solid rgba(255,255,255,.95); border-left:5px solid #8A4FE0;
  background:linear-gradient(135deg,rgba(255,255,255,.85),rgba(255,226,240,.75))}
.pw-next p{margin:0}
.pw-next .big{font-size:17px; line-height:1.4; font-weight:600}
.pw-next .small{font-size:13.5px; line-height:1.55; color:var(--pw-sec)}

/* request-sent card */
.pw-sent{display:flex; flex-wrap:wrap; align-items:center; gap:18px 26px; border-radius:24px; padding:22px 26px;
  background:linear-gradient(135deg,rgba(255,255,255,.75),rgba(205,230,255,.6))}
.pw-sent .orb{flex:none; display:flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:50%; background:var(--pw-grad);
  box-shadow:0 0 0 8px rgba(138,79,224,.14), 0 12px 28px rgba(91,87,232,.42)}
.pw-sent .body{flex:1 1 220px; min-width:0; display:flex; flex-direction:column; gap:4px}
.pw-sent .head{font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:700; font-size:32px; line-height:1.05; color:var(--pw-ink)}
.pw-sent .sub{font-size:14px; line-height:1.5; color:var(--pw-sec)}
.pw-ref{flex:none; display:flex; flex-direction:column; align-items:center; gap:2px; border-radius:16px; padding:10px 18px; background:rgba(255,255,255,.8); border:1px solid rgba(91,87,232,.3)}
.pw-ref b{font:700 24px/1.2 'Share Tech Mono',monospace; letter-spacing:.06em; color:var(--pw-ink)}

/* loading */
.pw-loading{display:flex; flex-direction:column; gap:14px}
.pw-loading .row{display:flex; align-items:center; gap:12px; font-weight:600}
.pw-dots{display:flex; gap:5px}
.pw-dots i{display:block; width:9px; height:9px; border-radius:50%; background:linear-gradient(135deg,#5B57E8,#C0408A); animation:pw-bob 1s ease-in-out infinite}
.pw-dots i:nth-child(2){animation-delay:.15s} .pw-dots i:nth-child(3){animation-delay:.3s}
.pw-shim{display:block; height:11px; border-radius:6px; margin-top:8px; background:linear-gradient(90deg,rgba(91,87,232,.12) 25%,rgba(91,87,232,.3) 50%,rgba(91,87,232,.12) 75%);
  background-size:200% 100%; animation:pw-shim 1.5s linear infinite}
.pw-steps{display:flex; flex-direction:column; gap:3px; font:13px/1.5 'Share Tech Mono',monospace; color:var(--pw-sec)}

/* simulation note under the composer */
.pw-note{margin:0; display:flex; flex-wrap:wrap; align-items:center; justify-content:center; gap:4px 10px; text-align:center;
  font:12px/1.5 'Share Tech Mono',monospace; letter-spacing:.03em; color:var(--pw-sec)}
.pw-note .pw-pill{padding:1px 10px; font-weight:700; letter-spacing:.12em}

/* sticky dock */
[data-testid="stLayoutWrapper"]:has(> .st-key-dock){position:sticky; bottom:0; z-index:20; padding:10px 0 4px}
[data-testid="stLayoutWrapper"]:has(> .st-key-dock)::before{content:""; position:fixed; left:0; right:0; bottom:0; height:230px; z-index:-1; pointer-events:none;
  background:linear-gradient(to top, rgba(238,241,255,.92) 45%, rgba(238,241,255,0))}
.st-key-dock{gap:12px !important}

/* ---------- primary / secondary buttons outside the composer ---------- */
[data-testid="stBaseButton-primary"], [data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--pw-grad); border:0; color:#fff; border-radius:999px; min-height:48px; padding:0 24px; font-weight:600;
  box-shadow:0 10px 24px rgba(91,87,232,.38), inset 0 1px 0 rgba(255,255,255,.35)}
[data-testid="stBaseButton-primary"] p, [data-testid="stBaseButton-primaryFormSubmit"] p{color:#fff; font-weight:600; font-size:14px}

/* ---------- dialogs (verify, talk to a person) ---------- */
[data-testid="stDialog"]{background:rgba(38,37,82,.3) !important; -webkit-backdrop-filter:blur(8px); backdrop-filter:blur(8px)}
[data-testid="stDialog"] div[role="dialog"]{
  border-radius:28px; background:rgba(255,255,255,.88); border:1px solid rgba(255,255,255,.95);
  -webkit-backdrop-filter:blur(26px) saturate(160%); backdrop-filter:blur(26px) saturate(160%);
  box-shadow:0 30px 80px rgba(60,50,150,.35), inset 0 1px 0 #fff; padding:10px 14px 14px}
[data-testid="stDialog"], [data-testid="stDialog"] p, [data-testid="stDialog"] label, [data-testid="stDialog"] button,
[data-testid="stDialog"] input, [data-testid="stDialog"] textarea, [data-testid="stDialog"] li{font-family:'Poppins',sans-serif}
[data-testid="stDialog"] :focus-visible{outline:3px solid var(--pw-ink) !important; outline-offset:3px !important}
[data-testid="stDialog"] [data-testid="stCaptionContainer"], [data-testid="stDialog"] [data-testid="stCaptionContainer"] *{color:var(--pw-sec) !important; opacity:1 !important}
[data-testid="stDialog"] [data-testid="stBaseButton-secondary"]{min-height:44px; padding:0 20px; border-radius:999px; border:1px solid rgba(91,87,232,.35); background:rgba(255,255,255,.7); color:var(--pw-ink)}
[data-testid="stDialog"] [data-testid="stBaseButton-secondary"]:hover{background:#fff; border-color:rgba(91,87,232,.5)}
[data-testid="stDialog"] [data-testid="stBaseButton-secondary"] p{font-size:14px; font-weight:600; color:var(--pw-ink)}
[data-testid="stDialog"] h2{font-family:'Poppins',sans-serif; font-size:21px; font-weight:600; color:var(--pw-ink)}
[data-testid="stDialog"] label p{font-size:13px; font-weight:600; color:var(--pw-ink)}
[data-testid="stDialog"] [data-testid="stCaptionContainer"]{color:var(--pw-sec); font-size:13.5px; line-height:1.55}
[data-testid="stDialog"] [data-testid="stTextInputRootElement"],
[data-testid="stDialog"] [data-baseweb="select"] > div,
[data-testid="stDialog"] [data-baseweb="textarea"]{
  min-height:48px; border:1.5px solid #6F6CCB !important; border-radius:14px !important; background:rgba(255,255,255,.85) !important}
[data-testid="stDialog"] input, [data-testid="stDialog"] textarea{color:var(--pw-ink) !important; font-size:15px; font-weight:500}
[data-testid="stDialog"] textarea::placeholder, [data-testid="stDialog"] input::placeholder{color:#4A4A7D !important; opacity:1}
[data-testid="stDialog"] [data-testid="stForm"]{border:0; padding:0}
[data-testid="stDialog"] [data-testid="stRadio"] [role="radiogroup"]{gap:10px}
[data-testid="stDialog"] [data-testid="stRadio"] [role="radiogroup"] > label{display:flex; align-items:center; min-height:44px; padding:0 18px 0 12px; margin:0;
  border:1.5px solid #6F6CCB; border-radius:999px; background:rgba(255,255,255,.8)}
[data-testid="stDialog"] [data-testid="stRadio"] [role="radiogroup"] > label p{font-size:14px; font-weight:500; color:var(--pw-ink); margin:0}

/* ---------- any other secondary button (Talk to a person, Back to start) ---------- */
[data-testid="stBaseButton-secondary"]{min-height:44px; padding:0 20px; border-radius:999px; border:1px solid rgba(91,87,232,.35); background:rgba(255,255,255,.7); color:var(--pw-ink)}
[data-testid="stBaseButton-secondary"]:hover{background:#fff; border-color:rgba(91,87,232,.5); color:var(--pw-ink)}
[data-testid="stBaseButton-secondary"] p{font-size:14px; font-weight:600; color:var(--pw-ink); margin:0}

[data-testid="stLayoutWrapper"]:has(> .st-key-scroll_hook){display:none}

/* ---------- motion ---------- */
@keyframes pw-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes pw-twinkle{0%,100%{opacity:1; transform:scale(1)}50%{opacity:.55; transform:scale(.82)}}
@keyframes pw-bob{0%,70%,100%{transform:translateY(0)}35%{transform:translateY(-5px)}}
@keyframes pw-shim{from{background-position:200% 0}to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){
  .pw-float,.pw-twinkle,.pw-dots i,.pw-shim{animation:none !important}
  .st-key-chips_home button, .st-key-chips_dock button{transition:none}
}

/* ---------- small screens ---------- */
@media (max-width:799px){
  /* pills wrap onto several rows here, so mirroring one row would over-pad; keep a moderate top gap */
  .st-key-composer_home{padding-top:30px}
}
@media (max-width:640px){
  [data-testid="stMainBlockContainer"]{padding:14px 16px 20px}
  .pw-word{font-size:30px}
  .pw-lede{font-size:15.5px}
  .st-key-composer_home{padding:30px 10px 10px 18px}
  [class*="st-key-turn_asst_"]{padding-left:0}
  [class*="st-key-turn_asst_"]::before{display:none}
  .pw-status{padding:16px}
  .pw-step-label{font-size:12px}
  .pw-sent .head{font-size:26px}
}
"""


def build_css() -> str:
    """The full stylesheet, with the inline image placeholders filled in."""
    css = (
        BASE_CSS.replace("__GRAIN__", svg_uri(_GRAIN))
        .replace("__ARROW__", svg_uri(_ARROW))
        .replace("__REFRESH__", svg_uri(_REFRESH))
        .replace("__AVATAR__", svg_uri(_AVATAR))
    )
    return FONT_IMPORT + css
