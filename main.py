#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second — make.fun entry.

One job: write a single sentence (at most 200 characters) to
/output/entry.txt, pitching a startup idea that sounds absurd at first
glance but turns out to be a real business.

The pitch: sell the naming rights to a home Wi-Fi network. It sounds
like a joke — who buys a router's name? — until you remember that
every phone in the building sees your network name while it hunts for
a signal, so the name is a tiny billboard, and brands already pay
monthly for far less visible ad space.

Standard library only, no network, deterministic: the same sentence
every run.
"""

import os
import sys

# The entry: one sentence, 142 characters. The absurd premise (selling
# a Wi-Fi network's name) turns on a real mechanism (SSIDs are
# broadcast to every nearby phone), and the money is named outright
# (brands pay $200 a month).
PITCH = (
    "We sell naming rights to your Wi-Fi network, because brands pay "
    "$200 a month to advertise to every phone in the building hunting "
    "for a signal."
)

MAX_CHARS = 200


def entry_stats(text):
    """Measure the entry once, so every gate below reads the same
    numbers instead of re-counting them ad hoc.

    Returns a dict with the character count, the number of terminal
    full stops, whether the text ends with one, and whether it holds
    any line break.
    """
    return {
        "chars": len(text),
        "stops": text.count("."),
        "ends_with_stop": text.endswith("."),
        "has_line_break": any(ch in text for ch in "\n\r"),
        "blank": not text.strip(),
    }


def validate(text):
    """Enforce the bounty gate: 1-200 characters, not only whitespace,
    exactly one sentence."""
    stats = entry_stats(text)
    if not text or stats["blank"]:
        raise ValueError("entry is empty or only whitespace")
    if stats["chars"] > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit"
            % (stats["chars"], MAX_CHARS)
        )
    # One sentence: a single terminal full stop, nothing else that
    # ends a sentence, no line breaks.
    if stats["stops"] != 1 or not stats["ends_with_stop"]:
        raise ValueError(
            "entry must be exactly one sentence "
            "(found %d full stop(s))" % stats["stops"]
        )
    if stats["has_line_break"]:
        raise ValueError("entry must not contain line breaks")
    return text


def main():
    entry = validate(PITCH)
    # An explicitly empty MAKEFUN_OUTPUT_DIR means "use the default",
    # not "write into the current directory".
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts every character, so the file
    # holds exactly the sentence, nothing more.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    stats = entry_stats(entry)
    print(
        "wrote %s (%d characters, %d sentence)"
        % (out_path, stats["chars"], stats["stops"])
    )
    print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
