# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. _"Retrieval works"_ is an opinion. _"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"_ is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; _"80% seemed reasonable"_ does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**

One of my five test questions asks about the CS 210 lab weighting, and that
fact lives in `course_cs_210.txt` right next to two sibling documents about
the same course (`course_cs_210_exams.txt`, `course_cs_210_workload.txt`).
Since those three documents are short and topically close, I expect retrieval
could pull a sibling instead of the one with the answer, so I'm not requiring
5 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

This doesn't depend on the answer being correct. Every chunk my pipeline
retrieves carries its source filename as metadata, and that filename always
gets included in the generated response's source line regardless of whether
the retrieved content actually answers the question. So all 5 is achievable;
the only way to miss it is a bug in the formatting step, not a bad retrieval.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**

I measured the best distance for all 5 in-corpus questions and all 5
`OUT_OF_SCOPE` questions with `python app.py retrieve`. The in-corpus best
distances ranged 0.19–0.36; the out-of-scope best distances ranged 0.82–0.93.
That's a wide, clean gap with nothing near the middle, so the default 0.6
cutoff sits safely inside it.

---

## 4. Answers come back fast

For at least 4 of my 5 in-corpus test questions, the system returns a full
answer within 10 seconds of the question being submitted.

**Why this target:**

Embeddings run locally on my own machine, so retrieval itself involves no
network call. The only real latency is one generation call to
`gemini-3.5-flash-lite`, a model built for speed, carrying a small prompt
since `campus_life` chunks are one to three short sentences each. 10 seconds
is generous for a single fast-model call; I'm not requiring 5 of 5 because
the first call of a session pays a one-time cost to load the local embedding
model, and any run can hit the rate limiter's backoff in `generate.py`.

---

## 5. Answers don't add claims the source doesn't make; mitigate hallucinations

For at least 4 of my 5 in-corpus test questions, every factual claim in the
generated answer is also stated in the retrieved chunk(s), it does not invent any
detail that isn't in the source.

**Why this target:**

`campus_life` posts are short, single-fact notes (one to three sentences), so
if the model pads an answer with extra specifics, they're easy to spot by
eye against the one short chunk that's supposed to be the whole source. I'm
not requiring 5 of 5 because a model asked to sound natural will sometimes
add a connecting phrase that isn't strictly false but also isn't in the text.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
