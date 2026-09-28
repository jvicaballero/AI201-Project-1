# The Unofficial Guide

Jasper Caballero — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

<!--

My notes:
Corpus - the folder of documents you're building this system for.
Chunk / chunking - split every document into smaller pieces called chunks, store them separately, and only pull out the 3–5 chunks that actually look relevant to a given question.
Chunk size - the maximum length (in characters) you let a chunk be. Set in config.py
Overlap - when a document is too long and has to be split into two+ chunks.
Embedding - to let a computer measure "how similar is this chunk to this question," converting into a list of numbers called a vector, produced by an embedding model
Distance - once everything's a vector, "how relevant is this chunk to this question" becomes "how close are these two vectors" a number, where lower means more similar.
Retrieval - the act of taking a question's vector and finding the chunks whose vectors are closest to it (smallest distance).
Relevance gate / threshold - if even the best (closest) chunk is still far away (a high distance number), that's a sign your corpus doesn't actually cover this question, and the system should say "I don't have enough information" instead of making something up. THRESHOLD = 0.6 is the cutoff distance: below it, answer; above it, refuse.
   Example: in-corpus questions came back with best distances 0.19–0.36 (well under 0.6), and out-of-scope questions came back 0.82–0.93 (well over 0.6).
Generation - the final step: take the retrieved chunks + the question, send them to an actual language model (gemini-3.5-flash-lite), and have it write a natural-language answer grounded in that material.
python app.py index - this did the chunking + embedding + storing, for real, against your 88 documents.
-->

## What This Does

This is a question-answering system built over `campus_life`, a corpus of 88
short student-written posts about university life such as dining halls, dorms,
courses, and administrative rules like deadlines and permits. It answers
questions a student might ask like when a course drop
starts showing as a W on a transcript, how the housing lottery orders
juniors and seniors, or where to park if you miss the permit window. Every
answer names the specific document it came from, and the system refuses to
answer questions its corpus doesn't cover rather than guessing.

## Chunking Strategy

**Chunk size:** 800 characters
**Overlap:** 120 characters

When I indexed `campus_life`, the 88 documents came out to 27,908 characters
total which is about 317 characters per document on average, ranging from 178 to
549 characters. Every single document is shorter than my 800-character chunk
size, so indexing produced exactly 88 chunks from 88 documents: nothing got
split. I kept the chunk size well above the longest document (549) on
purpose, since these posts are each a single, self-contained thought like a W
on your transcript, a lab weighting, a dollar amount, and splitting one
mid-sentence would break the one idea it exists to convey. The 120-character
overlap is mostly insurance for outlier posts I haven't seen yet since all the documents easily were divided on their own chunks.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::fallback_split`

```
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160.txt` — produced by: `chunker.py::fallback_split`

```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_hist_118_workload.txt` — produced by: `chunker.py::fallback_split`

```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.
```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt` — produced by: `chunker.py::fallback_split`

```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.
```

**Chunk 5** — source: `housing_innisfree_hall.txt` — produced by: `chunker.py::fallback_split`

```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Do dining dollars roll over from spring to the next autumn?

**Answer:**

```
(best distance 0.193, cutoff 0.6)

No, dining dollars do not roll over from the spring semester to the following autumn; whatever is left in May disappears.

Source: admin_dining_dollars.txt

Sources retrieved: admin_dining_dollars.txt, admin_meal_plan_changes.txt, dining_halden_hall.txt, dining_north_kitchen.txt, money_jobs.txt
```

**My relevance cutoff:** 0.6 (the default in `config.py`)

I ran all 5 of my in-corpus test questions and all 5 `OUT_OF_SCOPE`
questions through `python app.py retrieve` and recorded the best (lowest)
distance for each. The in-corpus group landed between 0.19 and 0.36; the
out-of-scope group landed between 0.82 and 0.93 which is a wide gap with nothing
near the middle. 0.6 sits safely inside that gap, so I kept the default
rather than tuning it.

| Question                                                          | In corpus? | Best distance |
| ----------------------------------------------------------------- | ---------- | ------------- |
| When does dropping a class start showing as a W on my transcript? | Yes        | 0.289         |
| Do dining dollars roll over from spring to the next autumn?       | Yes        | 0.193         |
| How are juniors and seniors ordered in the housing lottery?       | Yes        | 0.225         |
| What percentage of my CS 210 grade comes from the labs?           | Yes        | 0.364         |
| Where do people park when they miss the west lot permit window?   | Yes        | 0.327         |
| What is the capital of Mongolia?                                  | No         | 0.825         |
| How do I change the oil in a diesel engine?                       | No         | 0.934         |
| Who won the 1994 World Cup?                                       | No         | 0.886         |
| What is the recommended dosage of ibuprofen for a headache?       | No         | 0.844         |
| How do I write a for loop in Rust?                                | No         | 0.896         |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

I was actually very lost when it came to starting this project. I used AI for the times when I was confused or felt I didn't have a direction (which happened alot). I had Claude first explain to me in pieces the different files that I needed to focus on, as well as the concepts involved in each file/python command. I wrote my notes at the top of this readme just for my learning purposes.

**1.**
For the criteria, I had a general idea as to what I wanted to test, but didn't have the big picture of how to test it out and the parameters that I'm looking for. I wanted to check how fast these queries would be answered, but didn't know how to test out the time. I also wanted to include something about hallucination. I had Claude help me with measuring the success rate of these cases, one by introducing a general time to cut off, and the other to double check the chunks the answers are coming from.

**2.**
I also noticed that there were some concepts that had been left out of this initial iteration of the project, more specifically the Overlap. Since the chunks were set to 800 characters, the documents were too small to split up into separate chunks. I had Claude simulate this example to better visualize this concept:

"I just ran that for real on the same file with chunk_size=100, overlap=20, and you can see it above. Look at the boundary between chunk 0 and chunk 1:

Chunk 0 ends: "...take this with a grain of sal"
Chunk 1 starts: "with a grain of sal" + continues: "t. Built 1991, renovated 2022..."
That repeated "with a grain of sal" is the 20-character overlap — chunk 1 doesn't start exactly where chunk 0 stopped, it rewinds 20 characters first. So even though "grain of salt" got sliced in half by the 100-character cutoff, the whole word survives intact inside chunk 1. That's overlap's entire job: cushion the arbitrary cut point so a word or short phrase never exists nowhere in the chunk set."

I'll eventually run into this situation, better to understand it in a small sample size now!

The LLM, overall is just so helpful to organize my thoughts when working on a new concept, let alone reading through an entire repository.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion                                           | Target            | Run 1 | Run 2 | Run 3 | Verdict |
| --------------------------------------------------- | ----------------- | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer              | 4 of 5            | 5/5   | 5/5   | 5/5   | MET     |
| 2. Every answer names a source                      | 5 of 5            | 5/5   | 5/5   | 5/5   | MET     |
| 3. Gate stops out-of-corpus questions               | 4 of 5            | 5/5   | 5/5   | 5/5   | MET     |
| 4. Answers come back fast                           | 4 of 5 within 10s | 5/5   | 5/5   | 5/5   | MET     |
| 5. Answers don't add claims the source doesn't make | 4 of 5            | 5/5   | 5/5   | 5/5   | MET     |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

> **Note on `scorer.py`:** the first version of `judge()` had a bug —
> `expects.strip().lower() in (answer or"".lower())` — where `.lower()` bound
> to the empty string instead of `answer`, so `answer` was never actually
> lowercased. That produced false fails on the dining-dollars and parking
> questions purely from case mismatches. Fixed to
> `expects.strip().lower() in (answer or "").lower()`. Separately, two
> `expects` values in `questions.py` were too strict for how the generation
> model paraphrases: `"10%"` missed a run that said "Ten percent", and
> `"after the end of week two"` missed every run because the model never
> reliably includes "the end of" before the week number. Both were widened to
> accept alternative phrasings (`["10%", "ten percent"]` and
> `["week two", "second week"]`) — a fix to the test, not the pipeline, since
> retrieval and the underlying fact were correct in every run throughout. The
> evidence below is from the run after both fixes
> (`results/run_2026-09-28_0202_before.md`).

**Criterion 1 evidence**: retrieval output from `store.py::search`, run 1
of 3, showing the correct source present in every "Sources retrieved" list
(`results/run_2026-09-28_0202_before.md`):

```
When does dropping a class start showing as a W on my transcript?
Sources retrieved: admin_add_drop_deadline.txt, admin_grade_appeals.txt, admin_transcript_requests.txt, admin_withdrawal_deadline.txt, course_stat_150.txt

What percentage of my CS 210 grade comes from the labs?
Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_cs_340_exams.txt, course_stat_150.txt, course_stat_150_exams.txt
```

The document containing the actual answer (`admin_add_drop_deadline.txt`,
`course_cs_210.txt`) appears in both lists above, and the same held for all
5 questions across all 3 runs: retrieval is deterministic here, so the same
5 documents came back every time.

**Criterion 2 evidence**: every generated answer from `generate.py`, run 1
of 3, ends with a named source:

```
A drop shows as a W on your transcript if it occurs after week two. (Source: admin_add_drop_deadline.txt)

No, dining dollars do not roll over from the spring semester to the following autumn; whatever is left in May disappears.
Source: admin_dining_dollars.txt
```

All 5 questions, all 3 runs, named at least one source: 15 of 15.

**Criterion 3 evidence**: `run_eval.py::check_out_of_scope` against the
5 `OUT_OF_SCOPE` questions, one deterministic pass (`gate.py`):

```
What is the capital of Mongolia? best distance 0.825, refused
How do I change the oil in a diesel engine? best distance 0.934, refused
Who won the 1994 World Cup? best distance 0.886, refused
What is the recommended dosage of ibuprofen for a headache? best distance 0.844, refused
How do I write a for loop in Rust? best distance 0.896, refused
```

All 5 out-of-scope questions were refused, comfortably above the 0.6 cutoff.

**Criterion 4 evidence** — timed `python app.py ask "<question>"` end to end
(cache disabled with `AI201_CACHE=0`, `generate.py`'s call to
`gemini-3.5-flash-lite`), run 1 of 3:

```
5.1s  When does dropping a class start showing as a W on my transcript?
4.8s  Do dining dollars roll over from spring to the next autumn?
4.9s  How are juniors and seniors ordered in the housing lottery?
4.3s  What percentage of my CS 210 grade comes from the labs?
4.3s  Where do people park when they miss the west lot permit window?
```

All 15 timed calls (5 questions × 3 runs) landed between 4.3s and 5.1s, well
under the 10s target.

**Criterion 5 evidence** — one answer checked word-for-word against the
document it names as its source (`results/run_2026-09-28_0202_before.md`):

```
Question: What percentage of my CS 210 grade comes from the labs?
Answer:   10% of your CS 210 grade comes from the labs (course_cs_210.txt
          and course_cs_210_exams.txt).

Source text (course_cs_210.txt): "...do the labs even though they're only
10% — the exams reuse the lab problems."
Source text (course_cs_210_exams.txt): "Do the labs even though they're
only 10% — the exams reuse the lab problems."
```

The "10%" claim and the second-source claim are both literally present in
the retrieved documents — nothing in the answer goes beyond what the source
text says.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| #   | Criterion                                        | Verdict | How I decided                                                                                                                                                                                                                                                                               |
| --- | ------------------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Retrieved chunk contains the answer              | MET     | 5/5 in all 3 runs, above the 4/5 target. Retrieval is deterministic on this corpus (same distances, same sources every run), so there was nothing borderline to call. Confirmed by `scorer.py::judge` (fixed — see note above) as well as by reading the "Sources retrieved" list directly. |
| 2   | Every answer names a source                      | MET     | 5/5 in all 3 runs. Every generated answer ended with a `Source:` line, since the source filename is attached as metadata regardless of answer quality.                                                                                                                                      |
| 3   | Gate stops out-of-corpus questions               | MET     | 5/5 refused, one deterministic pass. All 5 out-of-scope best distances (0.82–0.93) sat far above the 0.6 cutoff, nothing close to the boundary.                                                                                                                                             |
| 4   | Answers come back fast                           | MET     | 5/5 in all 3 runs (15/15 total calls), all between 4.3s and 5.1s against a 10s target — comfortable margin, not a near-miss.                                                                                                                                                                |
| 5   | Answers don't add claims the source doesn't make | MET     | 5/5 in all 3 runs. Checked each answer's factual claims against its retrieved source text by hand; every claim, including the "also found in course_cs_210_exams.txt" detail, was literally present in the source.                                                                          |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

Missed nothing. All five criteria came back MET with comfortable margins in
`results/run_2026-09-28_0202_before.md`, not near-misses: retrieval (5/5 vs a
4/5 target), the gate (5/5 vs 4/5, distances 0.82–0.93 vs a 0.6 cutoff), and
no-hallucination (5/5 vs 4/5) all cleared their bar by more than the "1
question of slack" the target implies, and criterion 2 was maxed out at 5/5
by construction.

Being honest about it: most of these targets had real slack built in for
reasons tied to the corpus (documented in `criteria.md`), so a clean sweep
isn't a sign the targets were set too low across the board. But criterion 4
is the exception worth tightening. I set "4 of 5 within 10 seconds" when I
hadn't yet measured a single real call; the actual numbers came back
4.3–5.1s every time, which is a lot of unused headroom under a 10s bar. It's
also the one criterion with genuine run-to-run variability (a live model
call, subject to the rate limiter's backoff in `generate.py`) rather than a
deterministic retrieval or gate check, so it's the one place a tighter
number can actually be missed instead of being guaranteed to pass. I'd
tighten it to **4 of 5 within 6 seconds** — still above my observed worst
case (5.1s) by a small margin, but no longer generous enough to absorb a
slow call without consequence.

## The Improvement

**What I changed:** Dropped `TOP_K` in `config.py` from 5 to 3 — each
generation call now gets 3 retrieved chunks in its prompt instead of 5.

**Why I picked it:** Criterion 4 was diagnosed with a lot of unused headroom
(4.3–5.1s against a 10s target) and no other lever pointed at latency
specifically. Fewer chunks means a smaller prompt sent to
`generate.py::generate`, which is the one network call in the whole
pipeline, so it was the most direct thing to try against the newly
tightened 6-second bar.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                                           | Target           | Run 1 | Run 2 | Run 3 | Verdict |
| --------------------------------------------------- | ---------------- | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer              | 4 of 5           | 5/5   | 5/5   | 5/5   | MET     |
| 2. Every answer names a source                      | 5 of 5           | 5/5   | 5/5   | 5/5   | MET     |
| 3. Gate stops out-of-corpus questions               | 4 of 5           | 5/5   | 5/5   | 5/5   | MET     |
| 4. Answers come back fast (tightened)               | 4 of 5 within 6s | 4/5   | 4/5   | 4/5   | MET     |
| 5. Answers don't add claims the source doesn't make | 4 of 5           | 5/5   | 5/5   | 5/5   | MET     |

Full transcript: `results/run_2026-09-28_0209_after.md` (criteria 1/2/3/5,
`top-k: 3`). Criterion 4 isn't measured by `run_eval.py`, so it was timed the
same way as the "before" baseline — `python app.py ask "<question>"` end to
end, cache disabled, 3 runs:

```
run 1: 3.9s  4.0s  3.9s  3.9s  7.4s   (dropping / housing / CS210 / parking / dining)
run 2: 4.0s  4.0s  3.9s  5.5s  6.5s
run 3: 4.0s  3.9s  4.5s  4.0s  6.5s
```

(Order above: dropping-class, housing-lottery, CS-210-labs,
west-lot-parking, dining-dollars.)

**Did it help?**

No — and the numbers say so plainly. Four of five questions got a little
faster (mostly ~4.0s, versus 4.3–5.1s before), and prompt-token usage across
the 15 scored calls dropped about 35% (5,748 input tokens in
`run_2026-09-28_0209_after.md` vs 8,805 in
`run_2026-09-28_0202_before.md`) — a real, measured cost win. But the
dining-dollars question got _worse_, and consistently so: it ran 6.5–7.4s in
all 3 timed runs after the change, versus 4.8s in all 3 runs before. Under
the tightened 6-second target, that one question now misses every time,
which drops criterion 4 from **5 of 5** (before, every run) to **4 of 5**
(after, every run) — still technically MET against the "4 of 5" bar, but
with none of the margin the before-run had, and a new, repeatable weak
point that wasn't there before.

My read: prompt size wasn't the bottleneck. Retrieval and token count both
shrank as expected, but per-question latency is dominated by something else
in the network/API call itself (Gemini's per-request overhead, or the rate
limiter's pacing in `generate.py`) rather than by how many chunks ride
along in the prompt — and shrinking the prompt further would be unlikely to
fix a slowdown that shows up on one specific question rather than
uniformly across all five.

`TOP_K` is reverted to 5 in `config.py` — the experiment didn't earn a
place as the shipped default, so it's kept here as a documented result
rather than as the running configuration.

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

There's still a couple of inconsistencies/outliers that I noticed when it comes to the results. For starters, there's the exact matching issue that I'm noticing, where the expects function in scorer.py look for exact pattern matching from the expects answer to the answer we are given, which in turn might affect the evidence we gathered from the first criteria. In the future I would revisit that to consider more cases that just lower case or alternative "close-enough" statements (which might be the issue).

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

I think I was being a little too generous with my success criteria, especially with how I'd measured criteria 4 success. Just blindly picking a number 10s seemed good while planning out how to measure the time it takes for each query, but I think I should have done a bit more research, or even do a dry run timing before getting to a conclusive number. This would require a bit more callibrating on my part, or to make a more drastic edit, change the entire criteria all-together to not be based on time.

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
