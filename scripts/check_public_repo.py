from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "service-account.json",
    "secrets.json",
}

TEXT_EXTENSIONS = {
    ".py", ".md", ".toml", ".yml", ".yaml", ".json", ".txt", ".sh", ".ini", ".cfg", ".env", ""
}

# Deliberately target credential material, not ordinary words such as
# "private" in documentation. Example/template placeholders are allowed.
PATTERNS = {
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_pat": re.compile(r"\bghp_[A-Za-z0-9]{30,}\b"),
    "generic_secret_assignment": re.compile(
        r"(?im)^\s*(?:API_KEY|SECRET_KEY|PRIVATE_KEY|DATABASE_URL|DB_PASSWORD|JWT_SECRET|ANTHROPIC_API_KEY)\s*=\s*(?!$|YOUR_|CHANGE_ME|example|placeholder)([^\s#]{12,})"
    ),
}

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}


def iter_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    failures: list[str] = []
    for path in iter_files():
        rel = path.relative_to(ROOT)
        if path.name in FORBIDDEN_NAMES:
            failures.append(f"forbidden sensitive filename: {rel}")
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                failures.append(f"possible secret pattern {name}: {rel}")

    if failures:
        print("Public repository guard failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Public repository guard passed: no forbidden files or obvious credential material found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
