# Public Release Checklist

Use this checklist before a tagged release, external technical review, or major public-source update.

## Reproducibility

- [ ] Fresh install succeeds on Python 3.11 and 3.12.
- [ ] `python scripts/check_public_repo.py` passes.
- [ ] `python -m compileall -q src` passes.
- [ ] API/pipeline import smoke test passes.
- [ ] `ruff check src tests scripts` passes.
- [ ] `pytest -q` passes.
- [ ] `python examples/run_reference.py` produces non-empty output.
- [ ] Docker image builds successfully.

## Public-source safety

- [ ] No `.env`, private key, seed, API token, database credential, signing material, or user data is present.
- [ ] No production prompt, proprietary scoring/tuning, internal abuse threshold, operational runbook, or private infrastructure configuration is present.
- [ ] `.env.example` contains placeholders/public-safe defaults only.
- [ ] Public/private boundary documentation still matches the code.
- [ ] New copied production-derived code has been reviewed line-by-line for secrets and commercial IP.

## Reviewer experience

- [ ] README quick start matches the actual commands.
- [ ] Architecture diagram and code map match the repository.
- [ ] License is present and consistent with public source.
- [ ] Provenance describes production lineage without implying fake historical commits.
- [ ] Security policy gives a private-reporting route without requesting sensitive disclosure in public issues.
- [ ] CI checks are visible on the reviewed commit.
- [ ] External review references the exact commit/tag being evaluated.

A release is not considered verified merely because the files exist; the executable checks above must pass on the release commit.
