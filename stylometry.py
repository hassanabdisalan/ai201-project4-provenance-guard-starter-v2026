"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.

    Returns the coefficient of variation of sentence lengths (word counts):
    `stdev / mean`. Higher means MORE HUMAN — generated prose tends toward
    even, mid-length sentences, so a wide spread of short and long sentences
    next to each other is a human-ish trait. `style_signal` flips this before
    combining, since everything there has to point "higher = more AI".

    A submission with fewer than two sentences has no spread to measure —
    `stdev` raises on a single value — so that case returns 0.0 (reads as
    "no human-ish variation available," the conservative choice for a signal
    this flippable).
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns a float between 0 and 1. Higher means more varied vocabulary,
    which reads as MORE HUMAN — generated text tends to repeat a narrower
    band of common words. `style_signal` flips this before combining.

    Falls as text gets longer because common words repeat regardless of who
    wrote it, so this measure is only meaningful when comparing texts of
    similar length.
    """
    w = words(text)
    if not w:
        return 0.0
    return len(set(w)) / len(w)


def punctuation_density(text: str) -> float:
    """
    How much "interesting" punctuation appears, relative to word count.

    Counts semicolons, colons, dashes, and parentheses — not periods or
    commas, which are too common to tell writers apart. Returns a float
    (typically small, 0 to ~0.1) where higher means MORE HUMAN — this
    punctuation varies a lot between individual writers' habits and tends to
    flatten out in generated text. `style_signal` flips this before combining.
    """
    w = words(text)
    if not w:
        return 0.0
    interesting = re.findall(r"[;:()–—-]", text)
    return len(interesting) / len(w)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures below read MORE HUMAN as they go up (see each
    function's docstring), so each is flipped (`1 - clamped_measure`) before
    averaging, putting the combined result on the same "higher = more AI"
    scale as `detector.model_signal`.

    Each raw measure is clamped to a ceiling before the flip, so one outlier
    measure (e.g. unusually heavy semicolon use) can't make the whole score
    swing on its own:

      - sentence_length_spread: clamped to [0, 1.2] — coefficients of
        variation rarely exceed that for normal prose.
      - type_token_ratio: already 0–1, no clamp needed.
      - punctuation_density: clamped to [0, 0.08] — typical dense usage.

    The three flipped values are averaged with equal weight. Nothing here
    claims one measure matters more than another; Milestone 4's four
    calibration inputs are what would tell you if that's wrong.
    """
    spread = min(sentence_length_spread(text), 1.2) / 1.2
    ttr = min(type_token_ratio(text), 1.0)
    punct = min(punctuation_density(text), 0.08) / 0.08

    ai_from_spread = 1.0 - spread
    ai_from_ttr = 1.0 - ttr
    ai_from_punct = 1.0 - punct

    score = (ai_from_spread + ai_from_ttr + ai_from_punct) / 3.0
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
