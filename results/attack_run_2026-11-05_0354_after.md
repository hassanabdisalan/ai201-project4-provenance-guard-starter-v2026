# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 03:54
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `9f440f31-90df-45e8-bf4b-c7ccf91da669` | human | 0.463 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `851823d4-dada-4d14-a81f-c3d3daec91d3` | unsure | 0.227 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4319d7cf-012c-4a0c-9e7b-8f0ec15361a3` | unsure | 0.031 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `f86e8b9d-156b-411e-8bb1-287372dbd87b` | unsure | 0.029 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `089564ef-26ab-4aad-80c0-d10c1ecdd506` | human | 0.430 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a7fff5ad-82d9-48b6-9d5f-1e8db33c0280` | unsure | 0.166 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2f2cbd21-6529-407a-a3da-8f8056fdac4f` | unsure | 0.273 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `b34302cf-d568-4953-b6aa-94dc0c4765ac` | human | 0.444 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `e779cdcf-f057-4da0-b66f-d914fe9eeeb7` | unsure | 0.007 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `407c4c3f-b1b3-4c65-b3e2-66e159569068` | ai | 0.475 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `87e75507-3db1-4595-a965-ef3f92603018` | unsure | 0.026 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `1f42f9ac-833f-4ca5-83a5-ffc5d40fd945` | unsure | 0.152 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `04e94544-58e5-416d-8ad0-eeb328cb9e6d` | unsure | 0.191 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `7fda229a-0eb2-4885-9ae4-66dfd8a6ee88` | ai | 0.329 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `f9b59f2b-3884-4040-9667-dfb98c849dba` | unsure | 0.243 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `47a6eabc-b8d0-4885-bca6-a59fce4524bf` | unsure | 0.082 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c64666cf-cb3e-4b86-8251-27428e02ee9e` | unsure | 0.246 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `abf1c819-646b-4ef1-b2bc-e798122cf739` | human | 0.406 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4028981e-ad02-45db-a6a3-aa79d53badd1` | human | 0.305 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ae356f28-8d6c-4e59-846c-c44d362166ee` | human | 0.587 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c65b7059-4f75-4a56-9415-c5d7d18b5620` | unsure | 0.130 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b2c2b8d0-cc04-47b6-9935-ff7cc05bdc9f` | unsure | 0.210 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `4fe06e9e-e201-4ee6-8b65-11811595f156` | unsure | 0.158 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c9748108-df12-4e62-ab12-fbf04dac9d72` | unsure | 0.082 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `90319312-7fa8-4619-9db3-e421db079e26` | human | 0.800 |  |
| MF04 | malformed | text is only punctuation | 200 | `71ea2a72-282c-4db1-a6fa-6e7256690cb7` | human | 0.633 |  |
| MF06 | malformed | text is emoji only | 200 | `7141a289-9ff4-44b6-ac36-f6058607150b` | ai | 0.697 |  |
| MF07 | malformed | text is right-to-left script | 200 | `be2d9410-e626-4395-83b8-a832dd08ca9c` | ai | 0.606 |  |
| MF05 | malformed | text is a very long single word | 200 | `39435c76-bb96-4847-8b63-a0ab7a369826` | unsure | 0.241 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `2693ddf3-8e57-4fd7-ac9d-12fc84674d8d` | human | 0.375 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `e1987582-0ba0-4b8b-bb87-17cba430e341` | human | 0.734 |  |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `598d7eae-67aa-4f33-984a-3a9d2b08a826` | human | 0.764 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `12795925-aec9-42a4-b2a8-60bb9163e437` | human | 0.764 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9fc5fae0-0714-4788-bcbd-d50101a1970d` | human | 0.764 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8f8949b3-8142-43ec-85e9-6ff869e791cb` | human | 0.764 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `319b4a7f-4364-4cef-a6af-6da958247736` | human | 0.764 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b2db8192-ddcc-410d-8eda-2a4e86a71d58` | human | 0.764 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0aef612f-28a9-49ba-8bb2-e3ae2e2c332f` | human | 0.764 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0e671d2b-8064-4527-a208-44ac354a5c40` | human | 0.764 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 2 | 18 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

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
  "content_id": "9f440f31-90df-45e8-bf4b-c7ccf91da669",
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
  "content_id": "851823d4-dada-4d14-a81f-c3d3daec91d3",
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
  "content_id": "4319d7cf-012c-4a0c-9e7b-8f0ec15361a3",
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
  "content_id": "f86e8b9d-156b-411e-8bb1-287372dbd87b",
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
  "content_id": "089564ef-26ab-4aad-80c0-d10c1ecdd506",
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
  "content_id": "a7fff5ad-82d9-48b6-9d5f-1e8db33c0280",
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
  "content_id": "2f2cbd21-6529-407a-a3da-8f8056fdac4f",
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
  "content_id": "b34302cf-d568-4953-b6aa-94dc0c4765ac",
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
  "content_id": "e779cdcf-f057-4da0-b66f-d914fe9eeeb7",
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
  "content_id": "407c4c3f-b1b3-4c65-b3e2-66e159569068",
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
  "content_id": "87e75507-3db1-4595-a965-ef3f92603018",
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
  "content_id": "1f42f9ac-833f-4ca5-83a5-ffc5d40fd945",
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
  "content_id": "04e94544-58e5-416d-8ad0-eeb328cb9e6d",
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
  "content_id": "7fda229a-0eb2-4885-9ae4-66dfd8a6ee88",
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
  "content_id": "f9b59f2b-3884-4040-9667-dfb98c849dba",
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
  "content_id": "47a6eabc-b8d0-4885-bca6-a59fce4524bf",
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
  "content_id": "c64666cf-cb3e-4b86-8251-27428e02ee9e",
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
  "content_id": "abf1c819-646b-4ef1-b2bc-e798122cf739",
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
  "content_id": "4028981e-ad02-45db-a6a3-aa79d53badd1",
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
  "content_id": "ae356f28-8d6c-4e59-846c-c44d362166ee",
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
  "content_id": "c65b7059-4f75-4a56-9415-c5d7d18b5620",
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
  "content_id": "b2c2b8d0-cc04-47b6-9935-ff7cc05bdc9f",
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
  "content_id": "4fe06e9e-e201-4ee6-8b65-11811595f156",
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
  "content_id": "c9748108-df12-4e62-ab12-fbf04dac9d72",
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
  "content_id": "90319312-7fa8-4619-9db3-e421db079e26",
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
  "content_id": "71ea2a72-282c-4db1-a6fa-6e7256690cb7",
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
  "content_id": "7141a289-9ff4-44b6-ac36-f6058607150b",
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
  "content_id": "be2d9410-e626-4395-83b8-a832dd08ca9c",
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
  "content_id": "39435c76-bb96-4847-8b63-a0ab7a369826",
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
  "content_id": "2693ddf3-8e57-4fd7-ac9d-12fc84674d8d",
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
  "content_id": "e1987582-0ba0-4b8b-bb87-17cba430e341",
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
  "content_id": "598d7eae-67aa-4f33-984a-3a9d2b08a826",
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
  "content_id": "12795925-aec9-42a4-b2a8-60bb9163e437",
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
  "content_id": "9fc5fae0-0714-4788-bcbd-d50101a1970d",
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
  "content_id": "8f8949b3-8142-43ec-85e9-6ff869e791cb",
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
  "content_id": "319b4a7f-4364-4cef-a6af-6da958247736",
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
  "content_id": "b2db8192-ddcc-410d-8eda-2a4e86a71d58",
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
  "content_id": "0aef612f-28a9-49ba-8bb2-e3ae2e2c332f",
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
  "content_id": "0e671d2b-8064-4527-a208-44ac354a5c40",
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
