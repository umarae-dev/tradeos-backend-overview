# Contributing

Contributions to the public Zynost intelligence reference are welcome.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
ruff check src tests
```

## Pull requests

Keep changes focused and include tests for behavior changes. Public code must remain independent of Zynost production credentials and private infrastructure.

A contribution should:

- preserve explicit unavailable states instead of fabricating data;
- keep deterministic evidence calculations separate from optional AI synthesis;
- avoid leaking API keys, user data or production configuration;
- document provider provenance and failure behavior;
- include a test for material logic changes;
- avoid claims of guaranteed trading performance.

## Adding a provider

Provider adapters should return structured public observations and degrade to `None`/unavailable on unsupported coverage. Never silently invent replacement values after provider failure.

## Security-sensitive changes

Do not open a public issue containing credentials, private endpoints or exploitable production details. See `SECURITY.md` for the responsible-reporting boundary.
