"""All user-facing copy and canned prompts live here, so wording changes never touch layout code."""

APP_NAME = "Pathways AI"

# ---- Home screen ---------------------------------------------------------------------------
HERO_TITLE = "This is the Pathways AI simulation."
HERO_BODY = (
    "A test environment with fictional data. It explores how nonprofit professional-development "
    "programs could run admissions more easily, so the people who serve their communities spend "
    "less time on process and more on giving back."
)
COMPOSER_PLACEHOLDER_HOME = "Hi, I'm Pathways. Ask me about programs, admissions, or your application…"
COMPOSER_PLACEHOLDER_DOCK = "Ask about programs, admissions, or your application…"
DOCK_NOTE = "Fictional data, built as a test to make nonprofit professional-development admissions easier."

# ---- The three journeys: each tile sends exactly one canned message ------------------------------
EXPLORE_MESSAGE = "What do I need to apply for IT Support?"
STATUS_MESSAGE = "Where is my application?"
HUMAN_MESSAGE = "I'd like to talk to someone."

# icon: key into theme.ICONS, tint: gradient for the icon orb
TILES = [
    {
        "key": "explore",
        "title": "Explore programs",
        "message": EXPLORE_MESSAGE,
        "icon": "book",
        "tint": ("#FFE0EE", "#FFB3D6"),
        "badge": None,
    },
    {
        "key": "status",
        "title": "Check my application",
        "message": STATUS_MESSAGE,
        "icon": "clipboard",
        "tint": ("#E3F0FF", "#A6CDFF"),
        "badge": "ID CHECK",
    },
    {
        "key": "human",
        "title": "Talk to a person",
        "message": HUMAN_MESSAGE,
        "icon": "person",
        "tint": ("#EBE2FF", "#C5B2FF"),
        "badge": None,
    },
]

# ---- Suggested questions ---------------------------------------------------------------------
HOME_SUGGESTIONS = [
    "What programs start in January?",
    "What do I need to apply?",
    "How much does it cost?",
]
DEFAULT_SUGGESTIONS = ["Explore programs", "Check my application", "Talk to an advisor"]

# ---- Demo data used by the mock agent (all fictional) ----------------------------------------------
DEMO_EMAIL = "jordan.m@email.com"
DEMO_APPLICATION_ID = "APP-00482"
DEMO_NAME = "Jordan"
DEMO_PROGRAM = {
    "name": "IT Support Specialist",
    "chips": ["14 WEEKS", "EVENINGS", "NEXT START · JAN 11"],
}
DEMO_SOURCES = [
    {"title": "Admissions Guide 2026 · p. 4", "url": "#"},
    {"title": "IT Support Handbook · Requirements", "url": "#"},
]
DEMO_STAGES = ["Applied", "Documents", "Interview", "Decision"]
DEMO_CURRENT_STAGE = 1  # zero-based index into DEMO_STAGES
DEMO_NEXT_STEP = {
    "headline": "Upload your diploma or GED by Dec 3.",
    "detail": "Uploads happen in your applicant portal. I can't receive files here.",
    "link_label": "Open applicant portal",
    "link_url": "#",
}
DEMO_HANDOFF_REFERENCE = "HR-20418"

HANDOFF_TOPICS = ["My application", "Program questions", "Something else"]
HANDOFF_TIMES = ["Weekday mornings", "Weekday afternoons", "Evenings"]
HANDOFF_CONTACT = ["Email", "Phone"]
