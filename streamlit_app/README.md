# Pathways AI (simulation)

A chat front end for a fictional workforce-development nonprofit. It explores how professional-development
programs could run admissions more easily, so the people who serve their community spend less time on process
and more on giving back. **All data is fictional.** The UI is built in Streamlit; the agent behind it is
swappable. Today it is a mock. Next it will be a Salesforce Agentforce agent.

Three journeys, each started from a suggested question on the home screen (or by typing):

1. **Explore programs** - ask what's offered and what admissions require; get a program card and cited sources. The simulation covers one program, IT Support Specialist.
2. **Check my application** - verify identity, then see the current stage and the next required action.
3. **Talk to a person** - fill in a short request form, get a confirmation and a reference number.

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Demo identity for journey 2 is prefilled in the dialog (`jordan.m@email.com`, `APP-00482`).

Handy demo hooks:

- Type `simulate error` in the chat to see the friendly error state and the retry button.
- `PATHWAYS_MOCK_LATENCY=0` removes the artificial "thinking" delay (default 1.1 seconds).

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

`tests/test_agent.py` covers the mock agent. `tests/test_flows.py` drives all three journeys headlessly with
Streamlit's `AppTest`.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. At [share.streamlit.io](https://share.streamlit.io), choose **Create app**, pick the repository and branch,
   and set the main file path to `streamlit_app.py`.
3. Deploy. No secrets are needed while the backend is the mock.

Fonts (Cormorant Garamond, Poppins, Share Tech Mono) load from Google Fonts, so the app looks right when it
has internet access and falls back to system fonts without it.

## Project layout

```
streamlit_app.py        entry point: page setup, then home or conversation
pathways/
  content.py            all copy and demo data in one place
  agent.py              AgentClient protocol, MockAgent, SalesforceAgent stub
  ui.py                 session state, layout, dialogs, the request/response loop
  cards.py              HTML for program, sources, status and confirmation cards
  theme.py              the whole visual design (CSS, icons) injected once per run
tests/                  unit and end-to-end tests
.streamlit/config.toml  light theme and minimal toolbar
```

## How the Salesforce integration plugs in

The UI only talks to an `AgentClient` (`pathways/agent.py`): `send`, `verify`, `application_status` and
`request_handoff`. `MockAgent` implements them with canned, fictional answers. `SalesforceAgent` has the same
methods as stubs marked `TODO(salesforce)`, with an outline of the Agent API calls in its docstring.

To switch, fill in the stub and set `PATHWAYS_BACKEND=salesforce`. Put credentials in
`.streamlit/secrets.toml` locally or in the app's **Secrets** settings on Community Cloud. See
`.streamlit/secrets.toml.example` for the shape. That file is git-ignored; never commit real credentials.

## Known limits and post-MVP ideas

- **Header sign-in and "Talk to a person" pills** are left out on purpose. A real sign-in needs an auth
  callback to flip the state (`TODO(post-MVP)` in `ui.render_header`).
- **Progress track** is driven by a demo stage index. Salesforce will need to return a structured stage.
- **Typed messages** are routed by keywords in the mock. With the real agent, the agent decides when to ask
  for verification or a handoff, and returns that as `AgentReply.action`.
- **Sources** link to `#` placeholders.
