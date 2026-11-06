# Review guide

Give this file to every reviewer. Reviewers read dumped lessons (`courses/<spec>_lessons/NN_*.md`, raw `get_lesson` JSON) and the briefs (`courses/<spec>_outline.md`, block `### NN.`). They never read the token and make no network calls.

## Check, per lesson

1. Every claim, example, widget and practice. Verify anything non-obvious by running it (compiler, interpreter, calculator) or against a primary source.
2. Every multiple-choice practice: check every choice, not only the keyed one, and give the evidence per choice.
3. Every brief point: TAUGHT, MENTIONED, MISSING or WRONG.
4. No citing: any page, widget, keyword or practice that says "the book", "the course", "the article", "the author", "according to…" or sends the learner to a source instead of explaining.

## Severity

Counted (fails the lesson):
- a false statement;
- a wrong answer key or a second correct choice;
- an example shown as working that doesn't, or as failing that works;
- a rule stated more broadly than it holds, if a learner following it would get things wrong;
- citing a source instead of teaching;
- a page or practice that depends on a term the lesson (or an earlier lesson) never explains;
- a page that is only code or only a list, with no sentence saying what it shows.

Nit (reported, not counted): imprecise wording that leads to no wrong result, a gap the lesson fills elsewhere, clunky phrasing. When unsure, it is a nit.

## Output

`courses/review/<range>.md`, one block per lesson:

```md
## NN. Lesson name: PASS | FAIL
- counted: [kind] where: quote -> what is true. Evidence: ...
- nit: ...
```
