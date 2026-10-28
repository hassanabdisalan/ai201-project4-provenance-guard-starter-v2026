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

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take a weighted average of `model_score` and `style_score`,
style weighted higher because Milestone 1 showed the model signal is the one
that falsely accuses plain writers. Then, if the two signals disagree by 0.4
or more, treat that disagreement as real uncertainty rather than averaging it
away: pull the weighted result halfway toward whichever signal reads *more
human*. A wrong accusation costs a real writer more than a missed detection
costs the site, so when the two methods can't agree, the system should lean
toward not accusing — not split the difference as if disagreement meant
nothing.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.4`, `WEIGHT_STYLE_SIGNAL = 0.6`.
Disagreement threshold: `0.4`. All three are in `config.py`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

Lightly-edited AI text (typos and filler words stitched into a model-generated
paragraph) scored `model_score = 0.223` (the typos raised perplexity enough
to read as human-ish) but `style_score = 0.459` (the underlying sentence
structure is still too even and the vocabulary too narrow to read as human).
The gap is 0.236 — under my 0.4 disagreement threshold, so the rule just
weighted-averages them: `combined_score = 0.364`, landing just inside "unsure"
rather than "human". That's the case the disagreement rule exists for, even
though this particular gap wasn't wide enough to trigger it — it shows the
model signal alone would have under-called this one, and the style signal is
what kept it out of the "human" band.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



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
  -d '{"text": "I almost did not go to the party. Honestly almost bailed. But Maria texted me this dumb meme right as I was putting my shoes back on, and that was it, I was going. Glad I did -- the lasagna someone brought was unreal, and I ended up staying until 2am arguing about whether cereal counts as soup, which, for the record, it does not.", "creator_id": "hassan"}'
```

```json
{
  "combined_score": 0.3977,
  "confidence": 0.0,
  "content_id": "860efca4-1a9a-491d-b476-ef34e8267528",
  "guess": "unsure",
  "label": "PLACEHOLDER — labeling isn't built yet (Milestone 5).",
  "model_score": 0.4011,
  "style_score": 0.3954
}
```

<!-- Milestone 4: both signals and the combined score are wired in.
     guess/confidence/label are still placeholders — Milestone 5 adds the
     real label. -->

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": 0.3977,
      "content_id": "860efca4-1a9a-491d-b476-ef34e8267528",
      "creator_id": "hassan",
      "guess": "unsure",
      "label": "PLACEHOLDER — labeling isn't built yet (Milestone 5).",
      "model_score": 0.4011,
      "status": "decided",
      "style_score": 0.3954,
      "timestamp": "2026-10-28T23:13:18+00:00"
    }
  ]
}
```

<!-- The appeal sample and its log entry go here once /appeal is built in
     Milestone 5. -->

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
