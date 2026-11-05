"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

Criterion 4 (the appeal path) can't be tested by sending text alone — it
needs a submission first, then an appeal against the content_id that came
back. `run_eval.py`'s scenario shape has no place for that two-step flow, so
it's tested separately by `eval_appeal.py` (3 trials of 5 appeals each,
matching the "5 out of 5 tries" target), not through this file. That's a
deliberate choice, not an oversight — see the README's Run Log and
Verdicts section for how it's run and what came back.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "I went for a run this morning before it got too hot. Legs felt heavy for the first mile, then it evened out. Saw the same guy walking his dog by the bridge, like always.",
            "My desk is a mess right now. There's a coffee cup from Tuesday I keep meaning to wash, three notebooks I only use the first ten pages of, and a charger cable that belongs to a phone I don't own anymore.",
            "The bus was late again. I stood there for twenty minutes watching the little countdown on the sign go from 4 minutes to 9 minutes to 2 minutes, which doesn't make any sense but happens every single week.",
            "I tried a new recipe last night, a lentil soup thing. Put in too much cumin, not enough salt. Still ate two bowls of it anyway because I was hungry and didn't want to cook anything else.",
            "My sister called while I was in the middle of fixing a leaky faucet, and I answered with wet hands and regretted it immediately. We talked for forty minutes. The faucet is still leaking.",
            "Grading these submissions is slower than I expected. I keep having to stop and reread the same paragraph three times before I'm sure what the student was actually arguing.",
            "I forgot my umbrella again. Walked the last six blocks home in the rain, which was fine until my shoes started squeaking with every step and a stranger laughed at me at a crosswalk.",
            "We rearranged the living room over the weekend. The couch is in a spot that makes no sense now that I look at it in daylight, but moving it back feels like admitting defeat.",
            "I've been meaning to learn to play the guitar sitting in the corner of my room for about two years now. I pick it up maybe once a month, play the same four chords badly, and put it back down.",
            "The neighbor's cat has decided our porch is its porch now. It just sits there staring through the glass door until someone opens it, then walks in like it owns the place.",
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        # Clearly-AI and clearly-human, far enough apart that combined_score
        # should separate them by at least the 0.4 target in criteria.md.
        "texts": [
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.",
            "Rain. That's the first thing I remember about the day we moved into the lopsided little house on Carver Street, water sheeting off the gutterless roof in sheets thick enough to blur the moving truck into a smear of orange. Dad cursed. Mom laughed, which she almost never did on a bad day, and something about that cracked the tension wide open. We hauled boxes for six hours straight, soaked to the bone, and ate cold pizza sitting on upturned crates because the table hadn't arrived yet.",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        # Inputs spread across the score range, so all three labels are
        # actually reachable through a real submission, not just the thresholds
        # in config.py.
        "texts": [
            "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.",
            "Rain. That's the first thing I remember about the day we moved into the lopsided little house on Carver Street, water sheeting off the gutterless roof in sheets thick enough to blur the moving truck into a smear of orange. Dad cursed. Mom laughed, which she almost never did on a bad day, and something about that cracked the tension wide open. We hauled boxes for six hours straight, soaked to the bone, and ate cold pizza sitting on upturned crates because the table hadn't arrived yet.",
            "The committee reviewed the proposal on Tuesday. Members raised concerns about the budget. A revised draft will be submitted next week. The chair thanked everyone for their time and closed the meeting shortly after four o'clock.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        # 3 tries for each of the three malformed cases named in criteria.md:
        # missing text, empty text, and an oversized submission.
        "bodies": [
            {"creator_id": "eval_bad_missing_1"},
            {"creator_id": "eval_bad_missing_2"},
            {"creator_id": "eval_bad_missing_3"},
            {"text": "", "creator_id": "eval_bad_empty_1"},
            {"text": "", "creator_id": "eval_bad_empty_2"},
            {"text": "", "creator_id": "eval_bad_empty_3"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge_1"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge_2"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge_3"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
