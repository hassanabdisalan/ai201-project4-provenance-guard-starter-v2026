# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False positives

Of 10 submissions that are plain, honest writing I wrote myself, at most 1 may
come back labeled "high-confidence AI".

**Why this target:** On a writing site, a wrong accusation costs the writer
real standing and has no easy way to disprove; a missed piece of AI text just
costs the site one ungraded case. The expensive mistake is one-sided, so the
target for the costly direction has to be the tight one.

---

## 2. Score spread

Clearly-AI text (straight model output, unedited) and clearly-human text
(something plainly written, in my own words) must differ in `combined_score`
by at least 0.4, across all three trials.

**Why this target:** If the two obvious ends of the spectrum don't separate by
a wide margin, the signals aren't measuring anything real, and the whole
threshold band in between — where the hard cases live — is meaningless. 0.4 is
most of the 0–1 range, which is the bar a signal worth trusting should clear.

---

## 3. Label coverage

Each of the three labels — high-confidence human, unsure, high-confidence AI —
is actually produced by at least one real piece of text I submit, not just
mathematically reachable in `config.py`.

**Why this target:** A label that exists in the code but that no real
submission ever lands on isn't a working feature, it's a gap dressed up to
look like one. If I can't find text that produces it, a user never will
either, and the label is dead weight.

---

## 4. The appeal path

Every call to `/appeal` with a valid `content_id` changes that entry's status
to `under_review` and writes exactly one new log line, in 5 out of 5 tries.

**Why this target:** This is the only thing standing between a wrong
accusation and nothing at all for the person on the receiving end. It has to
work every single time I try it — a safety valve that works sometimes isn't
one a writer can rely on, and "sometimes" is not a number I'm willing to
accept here.

---

## 5. Bad input

Submitting `text` that is missing, empty, or roughly 50,000 words never
returns a 500 — it returns a 4xx with a clear reason, in 3 out of 3 tries for
each case.

**Why this target:** A crash on malformed input looks exactly like an outage
to the person who sent it, and gives them nothing to act on. These are also
the first inputs an attacker — or just a careless script — would try, so this
is the cheapest failure to prevent and the most embarrassing one to ship.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
