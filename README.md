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

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| #   | Criterion | Verdict | How I decided |
| --- | --------- | ------- | ------------- |
| 1   |           |         |               |
| 2   |           |         |               |
| 3   |           |         |               |
| 4   |           |         |               |
| 5   |           |         |               |

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

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion                              | Target | Run 1 | Run 2 | Run 3 | Verdict |
| -------------------------------------- | ------ | ----- | ----- | ----- | ------- |
| 1. Retrieved chunk contains the answer | 4 of 5 |       |       |       |         |
| 2. Every answer names a source         | 5 of 5 |       |       |       |         |
| 3. Gate stops out-of-corpus questions  | 4 of 5 |       |       |       |         |
| 4.                                     |        |       |       |       |         |
| 5.                                     |        |       |       |       |         |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
