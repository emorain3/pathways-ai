"""All user-facing copy and canned prompts live here, so wording changes never touch layout code."""

APP_NAME = "Pathways AI"

# ---- Home screen ---------------------------------------------------------------------------
HERO_TITLE = "This is the Pathways AI simulation."
HERO_BODY = [
    "An exploration of how automating parts of the admissions process could lower the barrier to entry, "
    "so learners feel clear about their next step instead of overwhelmed.",
    "This is a test environment with fictional data.",
]
COMPOSER_PLACEHOLDER_HOME = "Hi, I'm Pathways. Ask me about programs, admissions, or your application…"
COMPOSER_PLACEHOLDER_DOCK = "Ask about programs, admissions, or your application…"
DOCK_NOTE = "Fictional data, built as a test to make nonprofit professional-development admissions easier."

# ---- The three journeys: each starter pill sends exactly one canned message ------------------------
EXPLORE_MESSAGE = "What programs do you offer?"
STATUS_MESSAGE = "Where is my application?"
HUMAN_MESSAGE = "I'd like to talk to someone."

# Home screen: one starter per journey, kept general so visitors are not boxed into one question.
HOME_SUGGESTIONS = [EXPLORE_MESSAGE, STATUS_MESSAGE, HUMAN_MESSAGE]
# Fallback follow-ups inside a conversation when a reply does not suggest its own.
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
