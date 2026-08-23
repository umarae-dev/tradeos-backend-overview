## Summary

Describe the change and why it belongs in the public reference implementation.

## Public-source safety checklist

- [ ] No production credentials, secrets, private keys, tokens, database URLs, or user data are included.
- [ ] No proprietary production prompts, scoring/tuning, internal abuse thresholds, or operational runbooks are included.
- [ ] New behavior is covered by tests where practical.
- [ ] Documentation is updated if public behavior or architecture changes.
- [ ] `python scripts/check_public_repo.py` passes.
- [ ] `pytest -q` passes.

## Validation

List the commands or checks you ran.
