"""
Signal three (stretch): the stock-phrase signal.

Neither signal one nor signal two reads *what the text says*, only how
predictable or how shaped it is. This one looks at word choice directly — a
short list of phrases that show up disproportionately often in
LLM-generated prose ("it is important to note", "in conclusion",
"furthermore", "delve into", and similar hedge/transition filler) and counts
how often a submission uses them.

    from phrasing import phrase_signal
    score = phrase_signal("some text")   # 0.0 none found ... 1.0 saturated

**What it measures:** the rate of known AI-stock phrases per 100 words.
Unlike signal one or two, no direction-flip is needed — more hits always
means more likely AI, so this one already points the same way as
`detector.model_signal` and `stylometry.style_signal`.

**Why it might differ between human and AI writing:** these phrases are
disproportionately common in instruction-tuned model output — they're the
kind of safe, generic transition language a model reaches for by default.
A human writer uses some of them occasionally, but rarely clusters several
into one short submission.

⚠️ **The blind spot.** This is a fixed list. It catches exactly the phrases
it was given and nothing else — a model prompted to avoid them, or one from
a different era or vendor with different stylistic habits, slips through
untouched. And it runs backwards on anyone who happens to write in that
same hedge-y, academic register themselves: a human who overuses
"furthermore" and "it is important to note" by habit gets flagged by a
measure that has no way to tell voice from imitation. This signal is
lexical fingerprinting, not understanding — it is the easiest of the three
to defeat on purpose, and the first one worth throwing out if the attack
set in unit 8 shows it doing more harm than good.
"""

import re

_PHRASES = [
    "it is important to note",
    "it's important to note",
    "it is worth noting",
    "in conclusion",
    "in summary",
    "overall,",
    "furthermore,",
    "furthermore ",
    "moreover,",
    "moreover ",
    "additionally,",
    "on the other hand",
    "various factors",
    "plays a crucial role",
    "plays a pivotal role",
    "as an ai language model",
    "delve into",
    "in today's fast-paced world",
    "navigate the complexities",
    "a testament to",
    "rich tapestry",
    "boasts a",
    "stands as a",
]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Mirrors stylometry.words."""
    return re.findall(r"[a-z0-9']+", text.lower())


def phrase_hits(text: str) -> int:
    """How many times any stock phrase appears, case-insensitive."""
    lowered = text.lower()
    return sum(lowered.count(phrase) for phrase in _PHRASES)


def phrase_signal(text: str) -> float:
    """
    The stock-phrase signal as a 0–1 score. **Higher means more likely AI.**

    Rate is hits per 100 words. Three hits per 100 words (`RATE_CEILING`)
    saturates the score at 1.0 — one stray phrase in a long submission
    shouldn't swing the result, but a submission that leans on several of
    them should read as strongly AI-like on this signal alone.
    """
    word_count = len(words(text))
    if word_count == 0:
        return 0.0

    hits = phrase_hits(text)
    rate_per_100 = hits / (word_count / 100.0)

    RATE_CEILING = 3.0
    score = min(rate_per_100 / RATE_CEILING, 1.0)
    return round(score, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "It is important to note that, furthermore, this solution plays a "
        "pivotal role. In conclusion, one must delve into the various "
        "factors at play."
    )

    print(f"{len(words(text))} words, {phrase_hits(text)} stock-phrase hits\n")
    print(f"phrase_signal   {phrase_signal(text)}   (higher = more likely AI)")
