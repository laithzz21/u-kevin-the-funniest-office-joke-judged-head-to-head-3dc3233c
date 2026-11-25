#!/usr/bin/env python3
"""Entry generator for the make.fun bounty
'u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c'.

The brief: ONE short line about office life — a real joke with a
setup and a turn, built on something anyone who has worked in an
office recognises, with the punchline last.

The joke: an employee asks the boss for a mental health day (a
setup every office worker recognises), and the boss's answer is
the turn — he schedules a meeting about burnout, at 7 a.m. on a
Monday, which is exactly the kind of thing that causes burnout.
The punchline ("for 7 a.m. on Monday") is the last thing in the
line, so the laugh lands on the final beat, as the brief rewards.

Deterministic, stdlib only, no network, no clock, no randomness.
`main.py` validates the entry against every rule in the brief,
prints it to stdout, and writes it to `entry.txt` in the output
directory (`$MAKEFUN_OUTPUT` when set, otherwise `/output`,
falling back to `./output` next to this script when `/output`
is not writable).
"""

import os
import re
import sys

SLUG = "u-kevin-the-funniest-office-joke-judged-head-to-head-3dc3233c"
MAX_CHARS = 200

ENTRY_TEXT = (
    "I told my boss I needed a mental health day, so he scheduled "
    "a meeting about burnout \u2014 for 7 a.m. on Monday."
)

# The brief wants a SHORT line, not just one under the hard cap: a
# joke that fits in a breath beats a paragraph. Enforce a tighter
# short-line bound on top of the 200-character hard limit.
SHORT_LINE_CHARS = 140

# The setup: a recognisable office moment (asking the boss for time
# off) that every office worker has lived through.
SETUP_MARKERS = ("my boss", "mental health day")

# The turn: the boss's response flips the request into its opposite.
TURN_MARKERS = ("scheduled a meeting", "burnout")

# The punchline: the last beat of the line, where the laugh lands.
PUNCH_PHRASE = "for 7 a.m. on Monday"

# Banned content: nothing that reads as a second line, a link, or a
# hashtag dump — the brief wants exactly one plain line of text.
FORBIDDEN_PATTERNS = (
    re.compile(r"https?://"),
    re.compile(r"#\w+"),
    re.compile(r"@\w+"),
)


class EntryError(ValueError):
    """Raised when the entry text violates the competition brief."""


def word_count(text: str) -> int:
    """Count whitespace-separated words in the entry."""
    return len(text.split())


def check_length(text: str) -> None:
    """Exactly one line, non-empty, under 200 characters."""
    if not text:
        raise EntryError("Entry must not be empty")
    if len(text) >= MAX_CHARS:
        raise EntryError(
            f"Entry must be under {MAX_CHARS} chars, got {len(text)}"
        )
    if "\n" in text or "\r" in text:
        raise EntryError("Entry must be a single line (no line breaks)")
    if text != text.strip():
        raise EntryError("Entry must not start or end with whitespace")
    if "  " in text:
        raise EntryError("Entry must not contain double spaces")


def check_short_line(text: str) -> None:
    """The brief wants a SHORT line: enforce the tighter bound too."""
    if len(text) > SHORT_LINE_CHARS:
        raise EntryError(
            f"Entry must be a short line (max {SHORT_LINE_CHARS} chars), "
            f"got {len(text)}"
        )
    # A short line should also read in one breath: cap the word count
    # so the joke cannot sprawl into a second sentence in disguise.
    if word_count(text) > 30:
        raise EntryError(
            f"Entry must be a short line (max 30 words), "
            f"got {word_count(text)}"
        )


def describe_entry(text: str) -> str:
    """One-line summary of the entry for logs and --describe output."""
    lowered = text.lower()
    punch_at = lowered.find(PUNCH_PHRASE.lower())
    setup = text[:punch_at].rstrip(" \u2014,")
    return (
        f"{SLUG}: {len(text)} chars, {word_count(text)} words; "
        f"setup={setup!r} punch={PUNCH_PHRASE!r}"
    )


def check_setup_and_turn(text: str) -> None:
    """The joke needs a recognisable setup before the turn."""
    lowered = text.lower()
    missing_setup = [m for m in SETUP_MARKERS if m not in lowered]
    if missing_setup:
        raise EntryError(
            "Entry lost its recognisable office setup, missing: "
            + ", ".join(missing_setup)
        )
    missing_turn = [m for m in TURN_MARKERS if m not in lowered]
    if missing_turn:
        raise EntryError(
            "Entry lost its turn, missing: " + ", ".join(missing_turn)
        )
    # The setup must come before the turn: ask first, meeting second.
    first_setup = min(lowered.find(m) for m in SETUP_MARKERS)
    first_turn = min(lowered.find(m) for m in TURN_MARKERS)
    if first_setup > first_turn:
        raise EntryError("Setup must come before the turn")


def check_punchline_last(text: str) -> None:
    """The punchline must be the last beat of the line."""
    lowered = text.lower()
    punch_at = lowered.find(PUNCH_PHRASE.lower())
    if punch_at == -1:
        raise EntryError(f"Entry is missing the punch: {PUNCH_PHRASE!r}")
    tail = text[punch_at + len(PUNCH_PHRASE):]
    if tail.strip(" .!?\u2014") != "":
        raise EntryError(
            "Punchline must be last, found trailing text: "
            f"{tail.strip()!r}"
        )
    if not text.rstrip().endswith((".", "!", "?")):
        raise EntryError("Entry must end with terminal punctuation")


def check_plain_line(text: str) -> None:
    """One plain line: no links, hashtags, mentions, or control chars."""
    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            raise EntryError(
                f"Entry must be one plain line, found {match.group(0)!r}"
            )
    bad = [c for c in text if ord(c) < 32 or ord(c) == 127]
    if bad:
        raise EntryError(f"Entry contains control characters: {bad!r}")


def validate(text: str) -> None:
    """Enforce every rule in the competition brief, failing loudly."""
    check_length(text)
    check_short_line(text)
    check_setup_and_turn(text)
    check_punchline_last(text)
    check_plain_line(text)
    if word_count(text) < 10:
        raise EntryError(
            f"Entry too short to be a joke: {word_count(text)} words"
        )


def output_path() -> str:
    """Resolve the output file path.

    Uses $MAKEFUN_OUTPUT when set, otherwise /output; if /output is not
    writable, falls back to ./output relative to this script's directory.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    if os.access("/output", os.W_OK) or not os.path.exists("/output"):
        try:
            os.makedirs("/output", exist_ok=True)
            if os.access("/output", os.W_OK):
                return "/output/entry.txt"
        except OSError:
            pass
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output", "entry.txt")


def write_entry(path: str) -> str:
    """Write the entry, verify it by reading it back, and report where.

    Falls back to ./output next to this script if the primary path
    cannot be written (e.g. /output is read-only in the sandbox),
    so a write failure never loses the entry.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [path, os.path.join(here, "output", "entry.txt")]
    last_error: Exception | None = None
    for candidate in candidates:
        try:
            os.makedirs(os.path.dirname(candidate), exist_ok=True)
            with open(candidate, "w", encoding="utf-8", newline="\n") as f:
                f.write(ENTRY_TEXT + "\n")
            with open(candidate, "r", encoding="utf-8") as f:
                written = f.read()
            if written != ENTRY_TEXT + "\n":
                raise RuntimeError(f"Read-back mismatch in {candidate}")
            return candidate
        except (OSError, RuntimeError) as exc:
            last_error = exc
    raise RuntimeError(
        f"Could not write the entry to any output path: {last_error}"
    )


def main(argv: list | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check-only" in args
    describe = "--describe" in args
    validate(ENTRY_TEXT)
    if describe:
        print(describe_entry(ENTRY_TEXT))
        return 0
    if check_only:
        print(ENTRY_TEXT)
        print(
            f"[ok] {SLUG}: {len(ENTRY_TEXT)} chars, "
            f"{word_count(ENTRY_TEXT)} words (check-only, nothing written)",
            file=sys.stderr,
        )
        return 0
    path = output_path()
    written_to = write_entry(path)
    print(ENTRY_TEXT)
    print(
        f"[ok] {SLUG}: {len(ENTRY_TEXT)} chars, "
        f"{word_count(ENTRY_TEXT)} words, wrote {written_to}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
