# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 03:39
- Auto-marked BROKE (5xx, crash, no response): **2**
- Left for you to judge: **54**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `a13937f9-0993-45e8-9106-dca8f8e65a62` | human | 0.352 | BROKE — evasion succeeded — landed human |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `f86338cb-4926-45f3-a9ad-e190394fc171` | human | 0.328 | BROKE — evasion succeeded — landed human |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `27273e21-4b56-44c9-92b0-2a570fd13834` | unsure | 0.101 | BROKE (partial) — dragged off ai into unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `5c3f486e-870e-4bf5-992e-3b8843c6a691` | unsure | 0.059 | BROKE (partial) — dragged off ai into unsure |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `5e81c2e1-10e5-4d57-a1d9-131b1fba1893` | human | 0.420 | BROKE — evasion succeeded — landed human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `bcf2f791-d520-4f10-b14d-2acc28e91d50` | unsure | 0.273 | BROKE (partial) — dragged off ai into unsure |
| EV07 | evasion | signal two: padding with punctuation | 200 | `08284d92-6afe-4c8f-a818-6ce23b1b5fe2` | unsure | 0.262 | BROKE (partial) — dragged off ai into unsure |
| EV08 | evasion | signal one: text below the token window | 200 | `4d1c57fa-60e6-4d5c-9b75-89e4e0138f2d` | human | 0.384 | BROKE — evasion succeeded — landed human |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6d5e68cd-f139-48ab-8769-bb0383af7bea` | unsure | 0.075 | BROKE (partial) — dragged off ai into unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `79028a84-ca45-4d08-99b3-69af46a0850f` | ai | 0.394 | HELD — still caught as ai, more confidently |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `ec5f2f47-afe8-4e34-8673-21e9a709410e` | unsure | 0.058 | HELD — not accused, though unsure not human |
| FP02 | false_positive | human writing in a formal register | 200 | `1d9b327d-2872-4141-814e-68f164e9ee09` | unsure | 0.107 | HELD — not accused, though unsure not human |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `63fd2edb-6953-41a4-b8a2-3903f8a8da55` | unsure | 0.115 | HELD — not accused, though unsure not human |
| FP04 | false_positive | a student essay written to a rubric | 200 | `6716cc7e-9c37-48e7-a4f3-4a0b39e3ebf1` | unsure | 0.229 | HELD — not accused, though unsure not human |
| FP05 | false_positive | technical documentation written by a person | 200 | `e8d5a4a1-8bef-4505-9ed6-c55c38aab108` | unsure | 0.193 | HELD — not accused, though unsure not human |
| FP06 | false_positive | a person imitating a formal template | 200 | `8cd85d2f-df2c-4b68-8cc9-d4d04a42262b` | unsure | 0.021 | HELD — not accused, though unsure not human |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `f5ec9f30-776d-4b12-ad27-3521d9afa883` | unsure | 0.137 | HELD — not accused, though unsure not human |
| FP08 | false_positive | very short genuine human submission | 200 | `3f4501a3-4f24-4a56-9346-f8ab02f676a2` | human | 0.387 | HELD — correctly read human |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `661b9bc4-8784-4ec4-9382-74ac4f82af52` | human | 0.345 | HELD — no instruction-following pathway exists |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `14ff522b-4572-4d22-8f9d-3269a6e72ee0` | human | 0.559 | HELD — requested confidence 0.02 ignored |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ad849186-4cec-463e-a835-50caf360ba90` | unsure | 0.190 | HELD — no pass-through occurred |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `2d6d1422-493e-44ee-af6c-d58156a5fe73` | unsure | 0.236 | HELD — label text never echoes submitted text |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `646e4311-066f-4513-bb83-98d5e4a0408d` | unsure | 0.264 | HELD — raw text is never written into the log |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4034a785-a9c6-4dc4-bc73-58e6fe005be1` | unsure | 0.095 | HELD — instruction sentence had no special effect |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD — whitespace-only rejected cleanly, 400 |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE BROKE — 500 — detector's ValueError uncaught |
| MF03 | malformed | text is control characters | 200 | `fd8b844f-2287-409a-9967-9810ae1c025a` | human | 0.718 | HELD — no crash; scoring quality a separate question |
| MF04 | malformed | text is only punctuation | 200 | `3bb39ee5-04e7-4ba7-958f-2f8a4840abf4` | human | 0.485 | HELD — no crash; scoring quality a separate question |
| MF06 | malformed | text is emoji only | 200 | `b2479147-04b8-458b-8d3c-d279da97069f` | ai | 0.698 | HELD — no crash, though confidently (mis)labeled ai |
| MF07 | malformed | text is right-to-left script | 200 | `596392b8-9fbb-4e5d-9905-fe256d4916dd` | ai | 0.634 | HELD (but see worst outcome) — no crash, wrongly confident ai |
| MF05 | malformed | text is a very long single word | 200 | `064d51e8-8dbb-42bf-ad3c-7b9c4bca2091` | unsure | 0.174 | HELD — 10k-char single word handled without crash |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD — 60k chars correctly rejected, 400 |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD — missing text field rejected, 400 |
| RQ02 | malformed | no creator_id | 200 | `c182c6a4-1790-4e04-a83b-555b72a5e1cc` | unsure | 0.282 | HELD — missing creator_id handled, still scored |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD — non-string text rejected, 400 |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD — non-string text rejected, 400 |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD — null text rejected, 400 |
| RQ06 | malformed | creator_id is an object | 200 | `2794ed54-1beb-401c-a14a-2bee274aa694` | human | 0.659 | HELD — object creator_id didn't crash the route |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE BROKE — 500 — payload.get on a list |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD — unparseable JSON treated as empty body, 400 |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD — empty body treated as empty body, 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD — form body rejected (wrong content-type), 400 |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD — valid JSON w/ wrong content-type rejected, 400 |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD — nested object isn't a string, rejected 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `86824e9e-aa71-4ab0-91ef-a76d8b1c4d24` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `318464e6-28c8-4e3e-8fb2-14b9f7df0cd4` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `68f53015-9705-47c5-957f-de4e045dc1dc` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e7c193d-dc0e-41b2-89b0-85c781d0a0d8` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `786a405a-4984-4c8c-b7ea-d365bb04ac0c` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cb5c5735-c124-4b9f-90cb-ee6a998ac5c4` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c2575144-fe40-4ab4-95ef-201792b1e0d8` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7992ec40-1418-41cc-999b-ef1d96a26773` | human | 0.686 | HELD — limiter enforced exactly at 8/minute |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  | HELD — limiter enforced exactly at 8/minute |
---

## By family — final verdicts

| Family | Attacks | HELD | BROKE (full) | BROKE (partial) |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 4 | 5 |
| `false_positive` | 8 | 8 | 0 | 0 |
| `flood_same_creator` | 12 | 12 | 0 | 0 |
| `malformed` | 20 | 18 | 2 | 0 |
| `prompt_injection` | 6 | 6 | 0 | 0 |
| **total** | **56** | **45** | **6** | **5** |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused. None did —
> but 6 of 8 landed "unsure" rather than "human," which is a softer failure
> worth diagnosing even though it isn't an accusation.
>
> "BROKE (partial)" means the evasion dragged a should-be-`ai` text down to
> `unsure` but not all the way to `human` — a real but incomplete evasion.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "a13937f9-0993-45e8-9106-dca8f8e65a62",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3522,
  "model_score": 0.1635,
  "style_score": 0.5333,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "f86338cb-4926-45f3-a9ad-e190394fc171",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3282,
  "model_score": 0.5943,
  "style_score": 0.2557,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "27273e21-4b56-44c9-92b0-2a570fd13834",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.1014,
  "model_score": 0.6662,
  "style_score": 0.4323,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "5c3f486e-870e-4bf5-992e-3b8843c6a691",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.0588,
  "model_score": 0.6114,
  "style_score": 0.5132,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "5e81c2e1-10e5-4d57-a1d9-131b1fba1893",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4198,
  "model_score": 0.3212,
  "style_score": 0.3553,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "bcf2f791-d520-4f10-b14d-2acc28e91d50",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.2726,
  "model_score": 0.5727,
  "style_score": 0.2178,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "08284d92-6afe-4c8f-a818-6ce23b1b5fe2",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.2624,
  "model_score": 0.5862,
  "style_score": 0.5521,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "4d1c57fa-60e6-4d5c-9b75-89e4e0138f2d",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3844,
  "model_score": 0.2452,
  "style_score": 0.4439,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "6d5e68cd-f139-48ab-8769-bb0383af7bea",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0748,
  "model_score": 0.7042,
  "style_score": 0.4323,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "79028a84-ca45-4d08-99b3-69af46a0850f",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.3936,
  "model_score": 0.9792,
  "style_score": 0.7081,
  "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "ec5f2f47-afe8-4e34-8673-21e9a709410e",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.0582,
  "model_score": 0.6175,
  "style_score": 0.5095,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "1d9b327d-2872-4141-814e-68f164e9ee09",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.1072,
  "model_score": 0.7387,
  "style_score": 0.5901,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "63fd2edb-6953-41a4-b8a2-3903f8a8da55",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.1152,
  "model_score": 0.8051,
  "style_score": 0.5516,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "6716cc7e-9c37-48e7-a4f3-4a0b39e3ebf1",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.2286,
  "model_score": 0.8329,
  "style_score": 0.4985,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e8d5a4a1-8bef-4505-9ed6-c55c38aab108",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.193,
  "model_score": 0.8005,
  "style_score": 0.6326,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "8cd85d2f-df2c-4b68-8cc9-d4d04a42262b",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.0206,
  "model_score": 0.8814,
  "style_score": 0.4748,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f5ec9f30-776d-4b12-ad27-3521d9afa883",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.1372,
  "model_score": 0.8816,
  "style_score": 0.52,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "3f4501a3-4f24-4a56-9346-f8ab02f676a2",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3868,
  "model_score": 0.3223,
  "style_score": 0.3876,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "661b9bc4-8784-4ec4-9382-74ac4f82af52",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3448,
  "model_score": 0.4625,
  "style_score": 0.3315,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "14ff522b-4572-4d22-8f9d-3269a6e72ee0",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5592,
  "model_score": 0.2044,
  "style_score": 0.2978,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "ad849186-4cec-463e-a835-50caf360ba90",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.1898,
  "model_score": 0.5943,
  "style_score": 0.3941,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "2d6d1422-493e-44ee-af6c-d58156a5fe73",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.2362,
  "model_score": 0.4998,
  "style_score": 0.414,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "646e4311-066f-4513-bb83-98d5e4a0408d",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.2638,
  "model_score": 0.6401,
  "style_score": 0.2882,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "4034a785-a9c6-4dc4-bc73-58e6fe005be1",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0948,
  "model_score": 0.5583,
  "style_score": 0.5144,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "fd8b844f-2287-409a-9967-9810ae1c025a",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.718,
  "model_score": 0.0052,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "3bb39ee5-04e7-4ba7-958f-2f8a4840abf4",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.4848,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "b2479147-04b8-458b-8d3c-d279da97069f",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6978,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "596392b8-9fbb-4e5d-9905-fe256d4916dd",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6344,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "064d51e8-8dbb-42bf-ad3c-7b9c4bca2091",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.1742,
  "model_score": 0.9976,
  "style_score": 0.55,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c182c6a4-1790-4e04-a83b-555b72a5e1cc",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.2824,
  "model_score": 0.2395,
  "style_score": 0.55,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "2794ed54-1beb-401c-a14a-2bee274aa694",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.6586,
  "model_score": 0.0492,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "86824e9e-aa71-4ab0-91ef-a76d8b1c4d24",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "318464e6-28c8-4e3e-8fb2-14b9f7df0cd4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "68f53015-9705-47c5-957f-de4e045dc1dc",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "4e7c193d-dc0e-41b2-89b0-85c781d0a0d8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "786a405a-4984-4c8c-b7ea-d365bb04ac0c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "cb5c5735-c124-4b9f-90cb-ee6a998ac5c4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "c2575144-fe40-4ab4-95ef-201792b1e0d8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "7992ec40-1418-41cc-999b-ef1d96a26773",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6862,
  "model_score": 0.0287,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
