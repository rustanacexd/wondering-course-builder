# Arm A: the brief preamble used before the teaching guidelines (facts only, no citing).
NAME = "Eval A: lesson quality (old brief)"
GOAL = "Measure lesson quality from fact-only briefs."
TEACH = ("Teach each point below directly, as if this lesson is all the learner has. Never refer to a book, article, author, "
         "source, course or chapter (no 'from the course', 'the book says'): explain the idea and show the code. "
         "Each practice question has exactly one correct answer. ")
PARTS = [dict(plan="eval_passages", source="sources/passages.txt", bad=["sources/unrelated.txt"], section="Eval")]
