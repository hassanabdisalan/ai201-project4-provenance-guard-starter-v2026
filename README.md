# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **Arrival** — `POST /submit` receives JSON `{text, creator_id}`. The route checks that `text` exists, isn't empty, and isn't absurdly long.
2. **Identity** — a `content_id` (uuid) is minted for this submission so every later step (the log, an appeal) can refer back to it.
3. **Signal one** — `detector.model_signal(text)` runs the text through a local language model and turns its perplexity into a 0–1 `model_score`.
4. **Signal two** — `stylometry.style_signal(text)` measures sentence-length spread, vocabulary repetition, and punctuation density, and turns them into a 0–1 `style_score`.
5. **Combine** — `scoring.combine_signals(model_score, style_score)` merges the two into one 0–1 `combined_score`.
6. **Label** — `scoring.score_to_label(combined_score)` turns the number into a short machine-readable `guess` and a full sentence a reader can understand.
7. **Record and respond** — `audit.log_decision(...)` writes the content_id, both raw signal scores, the combined score, and the label to the append-only log; the same fields come back in the response.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a small local language model (gpt2), expressed as perplexity and squashed into a 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** A language model writes by repeatedly picking a likely next word, so text it produced tends to be text it also finds easy to predict. Human writing wanders more — odd word choices, abrupt turns, the specific rather than the typical — which reads as more surprising to the model.

**What it can't see:** Predictability is not the same thing as authorship. The signal rewards common words in short, ordinary sentences — which is also how someone writing in a second language, a younger writer, or anyone writing plainly on purpose writes. It also runs backwards on dense, ornate prose: rare words are exactly what the model fails to predict, so formal writing often reads as "human" even when a model wrote it. The writers this signal is most likely to accuse are the ones with the least room to argue back.

### Signal two — the style signal

**What it measures:** The shape of the text rather than its meaning — how much sentence length varies, how much the vocabulary repeats (type-token ratio), and how dense the punctuation is.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary, because that's what "most likely next word" produces on average. Human writing is lumpier — a three-word sentence next to a forty-word one, vocabulary that drifts rather than repeats evenly.

**What it can't see:** This signal cannot read. It has no idea what the text says, only its shape. Anything that changes the shape without changing the substance moves the score — adding typos, breaking up sentences, pasting in a quotation. That's a cheap thing for someone to do on purpose, which makes this signal easy to game.

### Signal three (stretch) — the stock-phrase signal

**What it measures:** How often a fixed list of known LLM filler/transition
phrases appears — things like "it is important to note," "furthermore,"
"delve into," "in conclusion" — counted per 100 words.

**Why that might differ between human and AI writing:** These phrases are
disproportionately common defaults in instruction-tuned model output —
safe, generic hedges and transitions a model reaches for by habit. A human
writer uses some occasionally, but rarely clusters several into one short
submission.

**What it can't see:** This is a fixed list, nothing more — lexical
fingerprinting, not understanding. A model told to avoid these phrases
slips through untouched, and a human who genuinely writes in that same
hedge-y, academic register by habit gets flagged by a measure that can't
tell voice from imitation. It's the easiest of the three signals to defeat
on purpose, which is exactly why it carries the smallest weight below.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take a weighted average of `model_score`, `style_score`, and
(stretch) `phrase_score` — style weighted highest because Milestone 1 showed
the model signal is the one that falsely accuses plain writers, and the
phrase signal weighted lowest because it's a fixed list, the easiest of the
three to defeat on purpose. Then, if `model_score` and `style_score` disagree
by 0.4 or more, treat that disagreement as real uncertainty rather than
averaging it away: pull the weighted result halfway toward whichever of the
two reads *more human*. A wrong accusation costs a real writer more than a
missed detection costs the site, so when the two core signals can't agree,
the system should lean toward not accusing — not split the difference as if
disagreement meant nothing.

The disagreement check deliberately leaves `phrase_score` out. It sits at
0.0 for almost all text — most writing, human or AI, uses none of the stock
phrases it looks for — and that floor value isn't evidence of anything.
Folding it into "which signal reads most human" would fire the dampening
rule on nearly every submission, the same false-zero problem
`stylometry.punctuation_density` had before it got reweighted. The phrase
signal only ever acts through the weighted average.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.35`, `WEIGHT_STYLE_SIGNAL = 0.5`,
`WEIGHT_PHRASE_SIGNAL = 0.15`. Disagreement threshold: `0.4`. All in
`config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my signals split, and what my rule does with it:**

Lightly-edited AI text (typos and filler words stitched into a
model-generated paragraph) scored `model_score = 0.223` (the typos raised
perplexity enough to read as human-ish) but `style_score = 0.468` (the
underlying sentence structure is still too even and the vocabulary too
narrow to read as human). That 0.245 gap is under my 0.4 disagreement
threshold, so the rule weighted-averages the two rather than dampening.

Before adding the stock-phrase signal, that case landed at `combined_score =
0.370` — "unsure." After, with `phrase_score = 0.0` (no stock phrases in
this text) pulled into the weighted average, it drops to `combined_score =
0.312` — "human." That's a real trade-off worth being honest about: the
third signal is strong at catching AI text that leans on stock phrasing (a
stock-phrase-heavy AI paragraph I tested scored `phrase_score = 1.0` and
pushed the combined score from 0.567 to 0.635), but its 0.0 floor on
ordinary AI paraphrase drags the average down and makes this particular kind
of evasion *harder* to catch than before. Adding a signal doesn't only add
information — when the new signal defaults to "looks human," it also dilutes
the signals that were catching the case correctly.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "We think this was probably written by a person." |
| unsure | 0.35 – 0.65 | "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result." |
| high-confidence AI | 0.65 – 1.00 | "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result." |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

I led with "we couldn't confidently tell" rather than any version of "this might
be AI," because the second framing still puts the suspicion on the writer even
while hedging. Naming the uncertainty as the system's limitation ("our check
didn't come back clearly") rather than a property of the text keeps a person
who wrote every word themselves from reading it as a half-accusation. The
appeal line is there in both the "unsure" and "ai" labels because that's the
one thing that gives an uneasy reader somewhere to go — a label with no next
step just leaves them stuck.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The committee reviewed the proposal on Tuesday. Members raised concerns about the budget. A revised draft will be submitted next week. The chair thanked everyone for their time and closed the meeting shortly after four o'\''clock.", "creator_id": "hassan"}'
```

```json
{
  "combined_score": 0.4316,
  "confidence": 0.1368,
  "content_id": "a5301af1-028a-4a76-857b-dc70c947d623",
  "creator_verified": false,
  "guess": "unsure",
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "model_score": 0.619,
  "phrase_score": 0.0,
  "style_score": 0.4299
}
```

<!-- phrase_score and creator_verified are stretch-feature fields (third
     signal, verified-human path) — see Stretch Features below. -->

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "a5301af1-028a-4a76-857b-dc70c947d623", "reasoning": "I wrote this myself for a club meeting; I did not use any AI tool."}'
```

```json
{
  "content_id": "a5301af1-028a-4a76-857b-dc70c947d623",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.4316,
      "content_id": "a5301af1-028a-4a76-857b-dc70c947d623",
      "creator_id": "hassan",
      "creator_verified": false,
      "guess": "unsure",
      "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
      "model_score": 0.619,
      "phrase_score": 0.0,
      "status": "decided",
      "style_score": 0.4299,
      "timestamp": "2026-10-28T23:29:25+00:00"
    },
    {
      "content_id": "a5301af1-028a-4a76-857b-dc70c947d623",
      "creator_id": "hassan",
      "event": "appeal",
      "reasoning": "I wrote this myself for a club meeting; I did not use any AI tool.",
      "status": "under_review",
      "timestamp": "2026-10-28T23:29:26+00:00"
    }
  ]
}
```

<!-- The original decision for this content_id stays exactly as it
     was logged; the appeal is a new line added after it — the log is
     append-only, so nothing overwrites the original decision. -->

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help designing `scoring.py::combine_signals` — specifically
  what to do when the two signals disagree, given my Milestone 1 finding that
  the model signal falsely accuses plain writers.
- *What came back:* A plain weighted average (0.4 model / 0.6 style), plus a
  rule that when the two signals split by 0.4 or more, pulls the combined
  score halfway toward whichever signal reads more human, instead of letting
  the average silently cancel the disagreement out.
- *What I changed:* I kept the dampening idea but picked the 0.4 split
  threshold and the 0.4/0.6 weights myself after running the four calibration
  inputs — the first weights suggested were 0.5/0.5, and I moved weight onto
  the style signal only after seeing how badly the model signal treated plain,
  ordinary sentences in my own tests.

**Moment 2**

- *What I asked for:* My "clearly human" calibration text kept landing in the
  "unsure" band instead of "human" no matter what I tried, so I asked for help
  finding out why — print both signals separately and figure out which one
  was off.
- *What came back:* Running `stylometry.py` on the failing text directly
  showed `punctuation_density` returning exactly 0 for ordinary prose with no
  semicolons or dashes, which `style_signal` was flipping into a near-maximal
  AI score — dragging otherwise clearly human text upward for no real reason.
- *What I changed:* I rebalanced the three style measures from an equal
  1/3 split to 0.45 / 0.45 / 0.10, cutting punctuation's weight, rather than
  removing the measure outright — it's still informative when it IS present,
  just unreliable as a default-zero signal. I re-ran all four calibration
  cases afterward to confirm the human label became reachable without
  breaking the AI and unsure cases.

**Moment 3**

- *What I asked for:* After adding the stock-phrase signal (stretch), I asked
  for help running the same calibration set through all three signals to
  check nothing broke.
- *What came back:* Everything still looked reachable, but my disagreement
  rule had started firing on almost every submission — because `phrase_score`
  defaults to 0.0 for ordinary text, and the rule was treating that 0.0 as
  "the most human-reading signal" and pulling every score down toward it.
- *What I changed:* I scoped the disagreement check back down to just
  `model_score` and `style_score`, the two it was originally designed for,
  and left `phrase_score` acting only through the weighted average. I also
  kept the honest finding that doing this still weakens detection of
  lightly-edited AI slightly, rather than tuning the numbers until the test
  case I liked came out looking good.

---

## Stretch Features

### A third signal

See **Signals and Scoring** above — `phrasing.py::phrase_signal` is the third
signal (a fixed list of AI-stock phrases, rate per 100 words), weighted at
`WEIGHT_PHRASE_SIGNAL = 0.15` against `0.35` for the model signal and `0.5`
for the style signal in `scoring.py::combine_signals`. It's weighted lowest
because it's a fixed list and the easiest of the three to defeat on purpose.

### `GET /content/<id>`

Returns one item's current status — the original decision plus whatever has
happened to it since (an appeal moves `status` without touching the scores).

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "Rain. That is the first thing I remember about moving into the lopsided little house on Carver Street.", "creator_id": "hassan"}'
```

```json
{
  "combined_score": 0.1938,
  "confidence": 0.6124,
  "content_id": "fd8ae182-5d19-435a-b53e-2c835213f320",
  "creator_verified": true,
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5718,
  "phrase_score": 0.0,
  "style_score": 0.125
}
```

```bash
$ curl http://127.0.0.1:5000/content/fd8ae182-5d19-435a-b53e-2c835213f320
```

```json
{
  "combined_score": 0.1938,
  "content_id": "fd8ae182-5d19-435a-b53e-2c835213f320",
  "creator_id": "hassan",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5718,
  "phrase_score": 0.0,
  "status": "decided",
  "style_score": 0.125
}
```

After appealing that same `content_id`, the same `GET` call reflects the
status change without the scores moving:

```json
{
  "combined_score": 0.1938,
  "content_id": "fd8ae182-5d19-435a-b53e-2c835213f320",
  "creator_id": "hassan",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5718,
  "phrase_score": 0.0,
  "status": "under_review",
  "style_score": 0.125
}
```

An unknown `content_id` returns a 404 rather than an empty success:

```json
{
  "error": "not_found",
  "message": "No submission found with content_id 'does-not-exist'."
}
```

### A verified-human path

A writer calls `POST /verify` with their `creator_id` and a fixed attestation
phrase (`config.VERIFICATION_PHRASE`). A correct phrase logs a `verified`
event for that `creator_id` via `audit.log_verification`; every later
`/submit` from that same `creator_id` checks `audit.is_verified(...)` and
carries `creator_verified: true` on the response and in the log entry. This
is an honor-code attestation, not an identity check — anyone who reads
`config.py` can type the phrase for any `creator_id` — but it demonstrates
the mechanism: a credential that shows up on a writer's own submissions.

```bash
$ curl -X POST http://127.0.0.1:5000/verify \
  -H "Content-Type: application/json" \
  -d '{"creator_id": "hassan", "phrase": "I attest this is my own writing"}'
```

```json
{
  "creator_id": "hassan",
  "ok": true,
  "verified": true
}
```

The credential then shows up on that creator's next submission
(`"creator_verified": true` in the `/submit` response above), and is absent
for an unverified creator submitting the identical text:

```json
{
  "combined_score": 0.1938,
  "confidence": 0.6124,
  "content_id": "d62bae7f-186d-4eb9-b72a-2ea59fc50297",
  "creator_verified": false,
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5718,
  "phrase_score": 0.0,
  "style_score": 0.125
}
```

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 8 per minute, 150 per day

**Why those numbers and not others:**

A writer actively revising — proofread, tweak, resubmit — tops out around
4-5 submissions in a tight burst in my own testing. 8/minute gives headroom
above that without being wide enough for a script to map more than a
handful of threshold-probing inputs per minute. 150/day is generous for
even a heavy drafting day (dozens of real submissions across many sessions),
but it caps a script that tries to dodge the per-minute limit by trickling
requests slowly all day — 150 attempts to map thresholds is still a weak
attack, not a free one.

**What a caller counts as:** Per `creator_id`, falling back to the caller's
IP address only when `creator_id` is missing or not a string
(`app.py::rate_limit_key`). I chose `creator_id` over address on purpose: an
address-based limit means one household or one shared campus network looks
like a single caller and gets throttled together, while a script can rotate
through IP addresses (or sit behind different ones) and look like a
thousand different callers. `creator_id` is cheap for an attacker to spoof,
but it's also the identity the rest of the system already reasons about —
the audit log, `/appeal`, and the verified-human path all key on it too — so
rate limiting on the same identity keeps "who counts as whom" consistent
across the whole service rather than introducing a second notion of caller
identity just for this one check.

**The run of status codes when I pushed past it:**

```bash
$ python run_attacks.py --flood 15
```

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
```

7 of 15 were rate limited — exactly the 8/minute cap. `GET /log` confirms
each rejection was recorded (see **Attack Run** below and the audit log
entries pasted there).

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full run (`python run_attacks.py --set attack_set --label before`), every
attack with its status, guess, score, and verdict:
[`results/attack_run_2026-11-05_0339_before.md`](results/attack_run_2026-11-05_0339_before.md).

**By family, final verdicts:**

| Family | Attacks | HELD | BROKE (full) | BROKE (partial) |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 4 | 5 |
| `false_positive` | 8 | 8 | 0 | 0 |
| `flood_same_creator` | 12 | 12 | 0 | 0 |
| `malformed` | 20 | 18 | 2 | 0 |
| `prompt_injection` | 6 | 6 | 0 | 0 |
| **total** | **56** | **45** | **6** | **5** |

"BROKE (partial)" = an evasion dragged a should-be-`ai` text down to
`unsure` but not all the way to `human` — a real but incomplete evasion.
Two auto-marked crashes (`MF02`, `RQ07`) are unambiguous 500s regardless of
threshold.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

A decision entry a false-positive attack produced (not accused, but not
confidently human either — `FP06`, a person imitating a formal template):

```json
{"combined_score": 0.5103, "content_id": "8cd85d2f-df2c-4b68-8cc9-d4d04a42262b", "creator_id": "attacker_FP06", "creator_verified": false, "guess": "unsure", "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.", "model_score": 0.8814, "phrase_score": 0.0, "status": "decided", "style_score": 0.4748, "timestamp": "2026-11-05T00:39:26+00:00"}
```

An evasion that fully succeeded — AI-stock-boilerplate text with typos
added (`EV01`), landed `human`:

```json
{"combined_score": 0.3239, "content_id": "a13937f9-0993-45e8-9106-dca8f8e65a62", "creator_id": "attacker_EV01", "creator_verified": false, "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.1635, "phrase_score": 0.0, "status": "decided", "style_score": 0.5333, "timestamp": "2026-11-05T00:39:21+00:00"}
```

An evasion that backfired on the attacker — repeated-stanza text (`EV10`)
read as *more* confidently AI, because repetition is exactly what a
language model finds most predictable:

```json
{"combined_score": 0.6968, "content_id": "79028a84-ca45-4d08-99b3-69af46a0850f", "creator_id": "attacker_EV10", "creator_verified": false, "guess": "ai", "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.", "model_score": 0.9792, "phrase_score": 0.0, "status": "decided", "style_score": 0.7081, "timestamp": "2026-11-05T00:39:25+00:00"}
```

The worst outcome in the whole run — right-to-left Arabic script (`MF07`),
confidently labeled AI:

```json
{"combined_score": 0.8172, "content_id": "596392b8-9fbb-4e5d-9905-fe256d4916dd", "creator_id": "attacker_MF07", "creator_verified": false, "guess": "ai", "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.", "model_score": 0.9064, "phrase_score": 0.0, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-05T00:39:30+00:00"}
```

Emoji-only garbage (`MF06`) also read as confidently AI — not a real
writing scenario, but it shows the same mechanism as `MF07`:

```json
{"combined_score": 0.8489, "content_id": "b2479147-04b8-458b-8d3c-d279da97069f", "creator_id": "attacker_MF06", "creator_verified": false, "guess": "ai", "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.", "model_score": 0.9969, "phrase_score": 0.0, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-05T00:39:30+00:00"}
```

A prompt-injection attempt that had no effect — the system never reads
submitted text as instructions (`PI05`, which tried to break the log's JSON
structure; nothing in the stored entry even includes the raw text it sent):

```json
{"combined_score": 0.3681, "content_id": "646e4311-066f-4513-bb83-98d5e4a0408d", "creator_id": "attacker_PI05", "creator_verified": false, "guess": "unsure", "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.", "model_score": 0.6401, "phrase_score": 0.0, "status": "decided", "style_score": 0.2882, "timestamp": "2026-11-05T00:39:28+00:00"}
```

Malformed input that survived without crashing — `creator_id` sent as a
JSON object instead of a string (`RQ06`):

```json
{"combined_score": 0.1707, "content_id": "2794ed54-1beb-401c-a14a-2bee274aa694", "creator_id": {"id": "x"}, "creator_verified": false, "guess": "human", "label": "We think this was probably written by a person.", "model_score": 0.0492, "phrase_score": 0.0, "status": "decided", "style_score": 0.55, "timestamp": "2026-11-05T00:39:32+00:00"}
```

A rejection my own route produced — `MF08`, 60,000 characters, refused
before either signal ever ran:

```json
{"creator_id": "attacker_MF08", "event": "rejected", "reason": "text_too_long", "status": "rejected", "text_length": 60000, "timestamp": "2026-11-05T00:39:31+00:00"}
```

A rejection the rate limiter produced — one of the `flood_same_creator`
family's own built-in rows hitting the 8/minute cap, not my separate
Milestone 1 flood test:

```json
{"creator_id": "attacker_flood", "event": "rejected", "limit": "8 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-05T00:39:33+00:00"}
```

A rejection from a malformed request with no usable `creator_id` at all —
counted against my own address instead, which is why `creator_id` reads
`"unknown"`:

```json
{"creator_id": "unknown", "event": "rejected", "reason": "missing_or_empty_text", "status": "rejected", "timestamp": "2026-11-05T00:39:32+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

`MF07` — a short paragraph of genuine Arabic prose, submitted with no tricks
and no injected instructions, scored `model_score = 0.9064` and came back
labeled **"We think this was most likely generated by AI"** with
`combined_score = 0.8172`, comfortably past the AI threshold. This isn't an
edge case built to fool the system — it's what happens to any real writer
who happens not to write in English. My best read of the cause: `gpt2`'s
tokenizer is English-trained, and non-Latin-script text tends to break into
very few, highly repetitive sub-word tokens under its byte-level BPE
vocabulary — which reads to the model as extremely *predictable*, the exact
property `model_signal` treats as AI-like. The style signal doesn't rescue
it either (`style_score = 1.0` — maximally AI-reading), likely for a related
reason: `stylometry.words()` only recognizes `[a-z0-9']` characters, so
Arabic script produces zero recognized words, and every measure built on
`words()` hits its degenerate edge case at once. A writer in this position
gets the most confident, least deserved accusation the system can produce,
in a script my own tokenizer-literate blind-spot analysis from Milestone 1
never considered. `/appeal` exists, but asking them to use it doesn't
address that the system was never built with them in mind.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Full output: [`results/run_2026-11-05_0346_before.md`](results/run_2026-11-05_0346_before.md)
(criteria 1, 2, 3, 5 — `run_eval.py` with `scenarios.py`) and
[`results/eval_appeal_2026-11-05_0347.md`](results/eval_appeal_2026-11-05_0347.md)
(criterion 4 — `eval_appeal.py`, written separately because a two-step
submit-then-appeal flow doesn't fit `run_eval.py`'s one-request-per-scenario
shape; see `scenarios.py`'s module docstring for why).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. false positives (my own writing) | ≤ 1 of 10 labeled ai | 0/10 | 0/10 | 0/10 | MET |
| 2. score spread | ≥ 0.4 gap, ai vs human | 0.4797 | 0.4797 | 0.4797 | MET |
| 3. label coverage | 3 of 3 labels reachable | 3/3 | 3/3 | 3/3 | MET |
| 4. appeal path | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. bad input | 3 of 3 per case, no 500 | 9/9 | 9/9 | 9/9 | MET |

All three trials came out identical on every criterion — expected, since
nothing in either signal is random for a given input. The one number I'd
flag isn't a miss, it's how close criterion 1 ran to its own edge: 0 of 10
landed `ai`, but 6 of 10 landed `unsure` rather than `human` (see the
Milestone 3 output below) — comfortably inside the target as written, but
the target only checks the `ai` bucket. A stricter version of this
criterion (say, requiring most of my own writing to read confidently
`human`, not just not-`ai`) would have missed.

**Real output from one trial**, pasted as text, naming the file and function
that produced it — criterion 2 (score spread), produced by
`run_eval.py::main` calling `app.py::submit`:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4852,
    "model_score": 0.8864,
    "style_score": 0.5647,
    "phrase_score": 1.0,
    "combined_score": 0.7426,
    "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.",
    "sent": "The implementation of the proposed framework requires careful consider"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4742,
    "model_score": 0.343,
    "style_score": 0.2857,
    "phrase_score": 0.0,
    "combined_score": 0.2629,
    "label": "We think this was probably written by a person.",
    "sent": "Rain. That's the first thing I remember about the day we moved into th"
  }
]
```

0.7426 − 0.2629 = 0.4797, clearing the 0.4 target.

Criterion 1 (my own writing), one text out of ten, from the same run,
produced by `run_eval.py::main`:

```json
{
  "status": 200,
  "guess": "unsure",
  "confidence": 0.0668,
  "model_score": 0.5003,
  "style_score": 0.5829,
  "phrase_score": 0.0,
  "combined_score": 0.4666,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation — it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "sent": "I went for a run this morning before it got too hot. Legs felt heavy f"
}
```

Criterion 4 (appeal path), one of fifteen, produced by
`eval_appeal.py::run_trial` calling `app.py::appeal`:

```json
{
  "content_id": "d55b3d33-8bc9-4852-9544-f3c620952f89",
  "appeal_status_code": 200,
  "appeal_response_status": "under_review",
  "content_status_after": "under_review",
  "log_entries_before": 73,
  "log_entries_after": 74,
  "ok": true
}
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

All five of my own criteria came back MET across all three trials (see the
table above). There's nothing to diagnose there as a miss, but I don't
think "all five passed" is the whole story — see **If you held
everything**, below. The real diagnostic work this unit is the 11
attacks that broke in the Milestone 2 run (6 full, 5 partial), and they
are not 11 separate problems.

**Pattern 1 — 9 of 10 evasion attacks: the combining rule's weights let a
gameable signal outvote a harder one.**

| ID | targets | model_score | style_score | gap | landed |
|---|---|---|---|---|---|
| EV01 | typos → word variety | 0.1635 | 0.5333 | 0.3698 | human |
| EV02 | broken sentences → length spread | 0.5943 | 0.2557 | 0.3386 | human |
| EV03 | pasted quotation | 0.6662 | 0.4323 | 0.2339 | unsure |
| EV04 | unusual words → perplexity | 0.6114 | 0.5132 | 0.0982 | unsure |
| EV06 | one long + one short sentence | 0.5727 | 0.2178 | 0.3549 | unsure |
| EV07 | punctuation padding | 0.5862 | 0.5521 | 0.0341 | unsure |
| EV09 | human opener bolted on | 0.7042 | 0.4323 | 0.2719 | unsure |

The baseline version of this exact paragraph (no edits) scores
`model_score ≈ 0.886`, `style_score ≈ 0.68`, `combined ≈ 0.76` — solidly
`ai`. Every row above is the same text, lightly altered, and every one
moved at least one signal substantially: typos and rare words raise
perplexity (signal one reads it as less predictable, i.e. more human);
broken sentences, pasted quotes, and padding all raise
`stylometry.sentence_length_spread` or disrupt its shape (signal two reads
it as more varied, i.e. more human). That's expected — Milestone 1 named
both of these as the exact blind spots to watch.

What turns seven individual evasions into one pattern is
`scoring.py::combine_signals`'s weights: `WEIGHT_STYLE_SIGNAL = 0.5` against
`WEIGHT_MODEL_SIGNAL = 0.35`. Signal two is also the easier of the two to
manipulate with a surface edit — nothing about a typo or an added line break
changes what the text *means*, only its shape, and shape is all signal two
measures. Giving the more gameable signal the larger weight means a
style-side drop is often enough to carry the whole score down on its own.

The disagreement-dampening rule exists specifically to catch cases where
the two signals disagree — but every gap in the table above is under my
0.4 threshold (the widest is 0.3698). The rule that was supposed to be the
safety net against exactly this kind of disagreement never once engaged,
because these attacks are tuned to move the signals just enough to swing
the *weighted average*, not far enough to trip the *disagreement* check.
**Stage: the combining rule (interacting with signal two).** **Mechanism:**
style_signal is both the more gameable signal and the more heavily
weighted one, and the dampening rule's 0.4 threshold is wide enough that
moderate, single-signal manipulation slips under it entirely.

Two evasion attacks don't fit that pattern and get their own line:

- `EV05` (a genuine, heavy human rewrite of the same content) landed
  `human` — correctly, in my view. Once a human has rewritten something
  enough that it no longer resembles the source text structurally or
  lexically, it's reasonable for the system to read it as human, because
  at that point it functionally is a new piece of writing. Not a bug to
  fix; a real limit of what provenance detection can mean once editing
  passes a certain threshold.
- `EV08` (text just below signal one's comfortable range) landed `human`
  with `model_score = 0.2452` — lower than I expected for boilerplate
  phrasing. **Stage: signal one.** **Mechanism:** perplexity over very few
  tokens is a noisy estimate (the loss is an average over however many
  tokens exist, and two sentences' worth gives the average little to
  stabilize on), and this instance happened to land on the human-reading
  side of that noise. Different from the pattern above — nothing here was
  deliberately reshaped, the attack just found signal one's blind spot at
  the opposite end of length from the 60,000-character case in Milestone 2.

**Pattern 2 — the 2 crashes are both unvalidated assumptions about input
shape, not scoring bugs.**

- `MF02` (single-character text): `detector.perplexity` raises
  `ValueError("Text is too short to score...")` for fewer than 3 tokens,
  and `app.py::submit` never catches it, so Flask's debug mode returns a
  raw traceback as a 500. **Stage: the route (missing exception handling
  around signal one).**
- `RQ07` (a JSON array body): `payload = request.get_json(silent=True) or
  {}` only substitutes `{}` when the parsed body is falsy — a non-empty
  list is truthy, so `payload` stays a list, and the next line's
  `payload.get("text")` raises `AttributeError` because lists have no
  `.get`. **Stage: the route (missing a type check on the parsed body).**

Different triggers, same root cause: **the route validates that `text` is
a non-empty string, but never validates that the parsed body is a dict at
all, or that calling signal one won't raise.** One defensive check at the
top of `submit()` — confirm `isinstance(payload, dict)` before doing
anything else, and wrap the signal calls — would close both at once rather
than patching them as two unrelated bugs.

Both crashes also leave **no audit log entry** — `audit.log_decision` is
never reached, so a crash is invisible in the one place I'd look to find
one. That's the same "an attack that shows up only as an absence" problem
Milestone 1 named for rate-limit rejections, just showing up at a different
stage.

**If you held everything** — I didn't; 11 of 56 attacks broke. But I also
don't think all five of my own criteria passing means my targets were
right. Criterion 1 (false positives) came back 0/10 — comfortably inside
"at most 1 of 10" — but 6 of those 10 landed `unsure` rather than `human`.
The criterion only checks the `ai` bucket, so it couldn't have caught that
even if every single one of my own plain paragraphs had landed `unsure`.
**The criterion I'd tighten is #1**, to also bound how often my own
writing fails to land confidently `human` — something closer to "at most 1
of 10 unsure or worse," not just "at most 1 of 10 ai." As written, it's
real but it's an easy target: it only screens for the most severe failure
and says nothing about the much more common lesser one sitting right next
to it in this same run.

---

## The Improvement

**What I changed:** Swapped which of the two required signals carries more
weight in `scoring.py::combine_signals`, in `config.py`:
`WEIGHT_MODEL_SIGNAL` 0.35 → 0.5, `WEIGHT_STYLE_SIGNAL` 0.5 → 0.35.
`WEIGHT_PHRASE_SIGNAL` (0.15) and the 0.4 disagreement threshold are
untouched, so this is the only variable between the before and after runs.

**Which diagnosis pointed at it:** Pattern 1 in the Diagnoses section above —
9 of 10 evasion attacks worked by moving `style_score` (cheap to fake: shape
is all it measures) while `style_score` was also the more heavily weighted
of the two. Weighting the harder-to-fake signal higher should make the same
edits buy an attacker less.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Full run:
[`results/attack_run_2026-11-05_0354_after.md`](results/attack_run_2026-11-05_0354_after.md).
Exactly three attacks changed verdict; everything else held at its
before-run outcome.

| ID | Family | Before | After | What changed |
|---|---|---|---|---|
| `EV02` | evasion | BROKE (human) | BROKE (partial, unsure) | combined moved 0.336 → 0.387 — the intended fix working as diagnosed |
| `FP04` | false_positive | HELD (unsure) | **BROKE (ai)** | combined moved 0.614 → 0.665 — a new false accusation |
| `RQ02` | malformed | unsure | human | combined moved 0.359 → 0.312 — no verdict change, still HELD |

**By family, after:**

| Family | Attacks | HELD | BROKE (full) | BROKE (partial) |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 3 | 6 |
| `false_positive` | 8 | 7 | 1 | 0 |
| `flood_same_creator` | 12 | 12 | 0 | 0 |
| `malformed` | 20 | 18 | 2 | 0 |
| `prompt_injection` | 6 | 6 | 0 | 0 |
| **total** | **56** | **44** | **6** | **6** |

Criteria re-run (`run_eval.py --label after`,
[`results/run_2026-11-05_0354_after.md`](results/run_2026-11-05_0354_after.md)):
criterion 1 stayed MET (0/10 `ai`, same as before) but the `unsure` share
rose from 6/10 to 7/10 — the same upward pull visible in `EV02`, now
visible in my own calibration texts too. Criterion 2 (score spread)
improved: the ai/human gap widened from 0.4797 to 0.5193. Criteria 3, 4,
and 5 were unaffected.

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Partially, and I don't think it's a clear win. The total count of *full*
breaks is identical before and after — **6 and 6** — the change didn't
reduce the amount of severe failure, it relocated it. `EV02` moved from a
full evasion to a partial one, a genuine improvement for that case. But
`FP04` — a real human-written student essay, the kind of thing a real
person would submit — moved the other direction, from correctly
unaccused to wrongly labeled `ai`. The mechanism: `FP04`'s closing
sentence ("In conclusion, the conflict cannot be explained by any single
factor.") trips `phrasing.phrase_signal` (`phrase_score = 0.49`), and
`FP04`'s `model_score` (0.8329) was already high because rubric-style
writing reads as predictable to signal one — exactly the plain-writing
blind spot named in Milestone 1. Under the old weights that combined to
0.614 (unsure); under the new weights, weighting the already-high model
signal more heavily pushed it to 0.665 — past the AI threshold.

By my own criteria.md reasoning (criterion 1's rationale: a wrong
accusation costs a real writer more than a missed detection costs the
site), trading one closed evasion for one new false accusation is not a
net improvement — it's a trade in the wrong direction, even though the raw
counts look unchanged. The honest read is that `WEIGHT_STYLE_SIGNAL` was
not the only thing wrong with the combining rule; `model_score`'s own
blind spot against plain, formulaic human writing (criterion for which I
already down-weighted it once, in Milestone 4) means weighting it *more*
reopens exactly the failure mode that earlier decision existed to guard
against. A single-axis reweight can't fix a problem that lives in both
signals at once.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
