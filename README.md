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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



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
