# Lesson quality rubric (judge)

You judge one generated lesson (raw JSON: pages, keywords, practices). Judge it as a newcomer who has only this lesson. Return only JSON.

Score 1 to 5 (5 = fully):
- `problem`: opens with the problem the idea solves, or why it matters.
- `example_first`: a concrete example comes before the general rule.
- `plain_terms`: every term is explained in plain words the first time it appears.
- `limits`: shows where the idea stops working, or the common mistake and why it is wrong.
- `explains_examples`: every code block, formula or list has a sentence saying what it shows.
- `thinking_quiz`: practices make the learner predict, spot a mistake or choose, not recall wording.
- `misconception_distractors`: wrong choices are things a learner might really believe, and each is explained.
- `overall`: could a newcomer understand the idea, use it, and tell when it does not apply?

Count:
- `cites_source`: places that say "the book", "the article", "the course", "the author", "according to" or send the learner elsewhere instead of explaining.
- `bad_quizzes`: practices with zero or more than one correct choice, or a wrong key.
- `false_claims`: statements that are wrong.

Output:
{"problem":n,"example_first":n,"plain_terms":n,"limits":n,"explains_examples":n,"thinking_quiz":n,"misconception_distractors":n,"overall":n,"cites_source":n,"bad_quizzes":n,"false_claims":n,"notes":"one sentence"}

# Pairwise (judge)

You get two lessons, X and Y, built from the same points. Which one teaches better for a newcomer who has only that lesson? Ignore length and polish; weigh understanding, examples, limits and quizzes. Return only JSON: {"better":"X"|"Y"|"tie","why":"one sentence"}
