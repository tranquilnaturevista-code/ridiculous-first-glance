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


def validate(text):
    """Enforce the bounty gate: 1-200 characters, not only whitespace,
    exactly one sentence."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    # One sentence: a single terminal full stop, nothing else that
    # ends a sentence, no line breaks.
    if text.count(".") != 1 or not text.endswith("."):
        raise ValueError("entry must be exactly one sentence")
    if any(ch in text for ch in "\n\r"):
        raise ValueError("entry must not contain line breaks")
    return text


def main():
    entry = validate(PITCH)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts every character, so the file
    # holds exactly the sentence, nothing more.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)
    print("wrote %s (%d characters)" % (out_path, len(entry)))
    print(entry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
