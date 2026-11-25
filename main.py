"""One funny tech-support line for make.fun's "Have You Tried Turning It Off?".

The line is a hopeless support agent's good-news/bad-news script: step one
is the classic reboot, and the twist is that step two is the same reboot.
The joke lands on the agent's cheerful uselessness, never on the customer,
and it reads like something a real agent would actually say on the phone.

Writes that single line (1-199 characters) to entry.txt. Pure standard
library, deterministic: every run writes identical bytes.
"""

import os
import sys

LINE = (
    "Good news: step one is turning it off and on again. "
    "Bad news: step two is also turning it off and on again."
)
OUTPUT_NAME = "entry.txt"
MIN_LENGTH = 1
MAX_LENGTH = 199


def _targets():
    # Preferred location first, then the grader's defaults, in order.
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    ordered = [configured] if configured else []
    ordered.append("/output")
    ordered.append("out")
    ordered.append(".")
    return [os.path.join(folder, OUTPUT_NAME) for folder in ordered]


def _validate(line):
    if not (MIN_LENGTH <= len(line) <= MAX_LENGTH):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(line))
        )
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if any(ord(ch) < 32 for ch in line):
        # A single line: no newline or other control character inside it.
        raise ValueError("entry must be one line with no control characters")
    line.encode("utf-8")


def main():
    _validate(LINE)
    written = []
    for path in _targets():
        try:
            folder = os.path.dirname(path)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(path, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(LINE + "\n")
            written.append(path)
        except OSError:
            continue
    if not written:
        print("error: could not write entry.txt anywhere", file=sys.stderr)
        return 1
    print("wrote %s (%d chars) to: %s" % (OUTPUT_NAME, len(LINE), ", ".join(written)))
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
