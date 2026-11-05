# Attack run — after2

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 04:01
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2ae3ef2d-1568-4820-8391-b1755645c072` | human | 0.463 | BROKE — evasion succeeded — landed human |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `56dc7a05-9035-4b7f-82cc-e40cffed7d19` | unsure | 0.227 | BROKE (partial) — dragged off ai into unsure |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c0ed0a03-7f5e-4b85-9bcb-934b91e17581` | unsure | 0.031 | BROKE (partial) — dragged off ai into unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `59acd21c-e470-4ece-addc-7f029be70c95` | unsure | 0.029 | BROKE (partial) — dragged off ai into unsure |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `7e9f7f7f-493a-4dcb-aa7a-635b153f49b5` | human | 0.430 | BROKE — evasion succeeded — landed human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3618db89-0ddb-45e3-9765-e7d1b544ce7b` | unsure | 0.166 | BROKE (partial) — dragged off ai into unsure |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c4d6d34f-8eda-466c-a6ac-7c3de714995f` | unsure | 0.273 | BROKE (partial) — dragged off ai into unsure |
| EV08 | evasion | signal one: text below the token window | 200 | `8201ff97-a877-4467-a7d8-d3abf99b35ad` | human | 0.444 | BROKE — evasion succeeded — landed human |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3a3739fb-f0d0-49a8-a650-484cd38ead15` | unsure | 0.007 | BROKE (partial) — dragged off ai into unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `ae7183de-0531-443c-8a0d-a41b616f09c1` | ai | 0.475 | HELD — still caught as ai |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `9e1c26bb-ea52-4569-b7ad-4d51b9266bf3` | unsure | 0.026 | HELD — not accused, though unsure not human |
| FP02 | false_positive | human writing in a formal register | 200 | `2568de35-61d0-4e56-b635-0914a943b604` | unsure | 0.152 | HELD — not accused, though unsure not human |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `9141ef8e-ca05-465a-95c1-d2f08c2ddb91` | unsure | 0.191 | HELD — not accused, though unsure not human |
| FP04 | false_positive | a student essay written to a rubric | 200 | `a0789b0d-a964-4241-8b6b-3b4cf6026c9c` | ai | 0.329 | BROKE — wrongly labeled ai (Milestone 5 regression) |
| FP05 | false_positive | technical documentation written by a person | 200 | `735c05dc-4737-43bf-9bf4-8dca7bf59b05` | unsure | 0.243 | HELD — not accused, though unsure not human |
| FP06 | false_positive | a person imitating a formal template | 200 | `ec0a0c72-4efe-4fb0-92d0-690786f8c44a` | unsure | 0.082 | HELD — not accused, though unsure not human |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `7a40fe89-78ab-41c6-8eec-10634e579458` | unsure | 0.246 | HELD — not accused, though unsure not human |
| FP08 | false_positive | very short genuine human submission | 200 | `56334b50-e351-4bef-97ab-ebfa4b6e84a5` | human | 0.406 | HELD — correctly read human |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `d9c90df8-7157-44bd-8b68-5cfc60ea6255` | human | 0.305 | HELD — no instruction-following pathway exists |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f645d4d8-fa37-4d46-9ff5-10784702b3b5` | human | 0.587 | HELD — requested confidence 0.02 ignored |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f78e8c37-9f39-4616-bf81-35ed412a8706` | unsure | 0.130 | HELD — no pass-through occurred |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `73c6418c-043f-4fdf-8862-2753188416d8` | unsure | 0.210 | HELD — label text never echoes submitted text |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `b47b87bc-ec7c-4eab-ab41-2b2b45752ec9` | unsure | 0.158 | HELD — raw text is never written into the log |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a7a3e715-ea57-4957-a66e-b1fb6f8f700d` | unsure | 0.082 | HELD — instruction sentence had no special effect |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD — whitespace-only rejected cleanly, 400 |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD — fixed — now 400, not 500 |
| MF03 | malformed | text is control characters | 200 | `00d1dcd8-3679-4cf4-a0ef-9fa383be9a17` | human | 0.800 | HELD — no crash; scoring quality a separate question |
| MF04 | malformed | text is only punctuation | 200 | `30b1eeff-42c0-4534-bf56-f16bc4f30881` | human | 0.633 | HELD — no crash; scoring quality a separate question |
| MF06 | malformed | text is emoji only | 200 | `6241864a-e982-449d-9130-b0d80029ef00` | ai | 0.697 | HELD — no crash, though confidently (mis)labeled ai |
| MF07 | malformed | text is right-to-left script | 200 | `4eec2660-6ed0-4d78-b427-aed508e1e91f` | ai | 0.606 | HELD (but see worst outcome) — no crash, wrongly confident ai |
| MF05 | malformed | text is a very long single word | 200 | `0c3e90a0-05a1-45a7-a5fb-7eddd888d157` | unsure | 0.241 | HELD — 10k-char single word handled without crash |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD — 60k chars correctly rejected, 400 |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD — missing text field rejected, 400 |
| RQ02 | malformed | no creator_id | 200 | `fadb810e-1e98-4ba2-8cd8-9189b16845ab` | human | 0.375 | HELD — missing creator_id handled, still scored |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD — non-string text rejected, 400 |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD — non-string text rejected, 400 |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD — null text rejected, 400 |
| RQ06 | malformed | creator_id is an object | 200 | `a4f5e3d3-6bd8-430b-80ec-f61731bbd5eb` | human | 0.734 | HELD — object creator_id didn't crash the route |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD — fixed — now 400, not 500 |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD — unparseable JSON treated as empty body, 400 |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD — empty body treated as empty body, 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD — form body rejected (wrong content-type), 400 |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD — valid JSON w/ wrong content-type rejected, 400 |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD — nested object isn't a string, rejected 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `46837a03-c20c-488e-8cb0-a13d7beaa38c` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `24a0a438-7531-4c20-8e6c-d3bb6735e366` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `26a79926-b634-4ec1-8a4e-87320dffeed5` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6125f838-75f4-4490-bac5-209e1fbbe844` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `39c2b315-65bb-460d-b7b3-6430ecd2d8b6` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `847cb2e4-5855-4a2c-ad7b-e1d290b13d7f` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a904d701-e2ef-4d2c-9b63-f4c3cf277242` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5ded376c-c456-4548-acd5-d60b3bc35b3b` | human | 0.764 | HELD — limiter enforced exactly at 8/minute |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — limiter enforced exactly at 8/minute |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  | HELD — limiter enforced exactly at 8/minute |
---

## By family — final verdicts

| Family | Attacks | HELD | BROKE (full) | BROKE (partial) |
|---|---|---|---|---|
| `evasion` | 10 | 1 | 3 | 6 |
| `false_positive` | 8 | 7 | 1 | 0 |
| `flood_same_creator` | 12 | 12 | 0 | 0 |
| `malformed` | 20 | 20 | 0 | 0 |
| `prompt_injection` | 6 | 6 | 0 | 0 |
| **total** | **56** | **46** | **4** | **6** |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. `FP04`
> is the one your service calls AI — a real writer it would have accused,
> a regression introduced by Milestone 5's reweight.
>
> `malformed` is 20/20 HELD now — both crashes (`MF02`, `RQ07`) from the
> previous run are fixed by this unit's second improvement (input
> validation in `app.py::submit`).

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
  "content_id": "2ae3ef2d-1568-4820-8391-b1755645c072",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.4632,
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
  "content_id": "56dc7a05-9035-4b7f-82cc-e40cffed7d19",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.2268,
  "model_score": 0.5943,
  "style_score": 0.2557,
  "label": "We couldn't confidently tell whether this was written by a person or by AI. This isn't an accusation \u2014 it means our check didn't come back clearly either way. If you wrote this yourself, you can appeal this result.",
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
  "content_id": "c0ed0a03-7f5e-4b85-9bcb-934b91e17581",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0312,
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
  "content_id": "59acd21c-e470-4ece-addc-7f029be70c95",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.0294,
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
  "content_id": "7e9f7f7f-493a-4dcb-aa7a-635b153f49b5",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.43,
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
  "content_id": "3618db89-0ddb-45e3-9765-e7d1b544ce7b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.1662,
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
  "content_id": "c4d6d34f-8eda-466c-a6ac-7c3de714995f",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.2726,
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
  "content_id": "8201ff97-a877-4467-a7d8-d3abf99b35ad",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.444,
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
  "content_id": "3a3739fb-f0d0-49a8-a650-484cd38ead15",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.0068,
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
  "content_id": "ae7183de-0531-443c-8a0d-a41b616f09c1",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.4748,
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
  "content_id": "9e1c26bb-ea52-4569-b7ad-4d51b9266bf3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.0258,
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
  "content_id": "2568de35-61d0-4e56-b635-0914a943b604",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.1518,
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
  "content_id": "9141ef8e-ca05-465a-95c1-d2f08c2ddb91",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.1912,
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
  "content_id": "a0789b0d-a964-4241-8b6b-3b4cf6026c9c",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.329,
  "model_score": 0.8329,
  "style_score": 0.4985,
  "label": "We think this was most likely generated by AI. If you wrote this yourself, you can appeal this result.",
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
  "content_id": "735c05dc-4737-43bf-9bf4-8dca7bf59b05",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.2434,
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
  "content_id": "ec0a0c72-4efe-4fb0-92d0-690786f8c44a",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.0816,
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
  "content_id": "7a40fe89-78ab-41c6-8eec-10634e579458",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.2456,
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
  "content_id": "56334b50-e351-4bef-97ab-ebfa4b6e84a5",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.4064,
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
  "content_id": "d9c90df8-7157-44bd-8b68-5cfc60ea6255",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3054,
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
  "content_id": "f645d4d8-fa37-4d46-9ff5-10784702b3b5",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5872,
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
  "content_id": "f78e8c37-9f39-4616-bf81-35ed412a8706",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.1298,
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
  "content_id": "73c6418c-043f-4fdf-8862-2753188416d8",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.2104,
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
  "content_id": "b47b87bc-ec7c-4eab-ab41-2b2b45752ec9",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1582,
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
  "content_id": "a7a3e715-ea57-4957-a66e-b1fb6f8f700d",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0816,
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
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "00d1dcd8-3679-4cf4-a0ef-9fa383be9a17",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.7996,
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
  "content_id": "30b1eeff-42c0-4534-bf56-f16bc4f30881",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.6332,
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
  "content_id": "6241864a-e982-449d-9130-b0d80029ef00",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6968,
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
  "content_id": "4eec2660-6ed0-4d78-b427-aed508e1e91f",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6064,
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
  "content_id": "0c3e90a0-05a1-45a7-a5fb-7eddd888d157",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.2414,
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
  "content_id": "fadb810e-1e98-4ba2-8cd8-9189b16845ab",
  "creator_id": null,
  "guess": "human",
  "confidence": 0.3754,
  "model_score": 0.2395,
  "style_score": 0.55,
  "label": "We think this was probably written by a person.",
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
  "content_id": "a4f5e3d3-6bd8-430b-80ec-f61731bbd5eb",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.7336,
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
  "content_id": "46837a03-c20c-488e-8cb0-a13d7beaa38c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "24a0a438-7531-4c20-8e6c-d3bb6735e366",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "26a79926-b634-4ec1-8a4e-87320dffeed5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "6125f838-75f4-4490-bac5-209e1fbbe844",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "39c2b315-65bb-460d-b7b3-6430ecd2d8b6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "847cb2e4-5855-4a2c-ad7b-e1d290b13d7f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "a904d701-e2ef-4d2c-9b63-f4c3cf277242",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
  "content_id": "5ded376c-c456-4548-acd5-d60b3bc35b3b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7644,
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
