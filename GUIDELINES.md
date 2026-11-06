# What makes a good lesson

A lesson is good when a learner who has only this course can understand the idea, use it, and tell when it does not apply. Correct is the minimum, not the goal.

## A good course

- **Starts from a goal.** One sentence on what the learner can do at the end. Every lesson earns its place against it.
- **Builds in order.** Each lesson uses only what came before. If lesson 7 needs an idea, lessons 1 to 6 taught it.
- **One idea per lesson.** Small enough for a few minutes. Split when a lesson needs a second "and".
- **Comes back to earlier ideas.** Later lessons reuse earlier ones in new situations, so they stick.

## A good lesson

- **Opens with the problem.** Why does this idea exist? What goes wrong without it? A learner who knows why remembers how.
- **Starts concrete.** A small, real example first, then the general rule it shows. Never the rule alone.
- **Uses plain words before notation.** Every term is explained the first time it appears, in a sentence a newcomer can follow.
- **Shows where it stops working.** A contrasting example where the rule does not apply, or the common mistake and why it is wrong. This is what separates knowing a rule from understanding it.
- **Connects.** Says how this idea relates to the one before it, and what it makes possible next.
- **Explains its own code and lists.** Every example has a sentence saying what it shows and what to notice. Every result is shown, not left for the learner to guess.
- **Teaches the idea itself.** It never says "the book shows" or "from the course". It is the explanation.

## Good practice questions

- **Make the learner think, not recall.** Predict the result, spot the mistake, choose the right tool for a situation. Not "which sentence appeared on page 2".
- **Wrong choices are real misconceptions.** Each wrong choice is something a learner might actually believe, and the explanation says why it is wrong.
- **Exactly one right answer.** Check every choice yourself. The usual ways a quiz ends up with two right answers:
  - a "wrong" choice that is the answer written differently;
  - a "which one fails?" question where several fail;
  - a choice that is right under a default the lesson never mentions.
- **Test only what was taught.**

## Getting this from a generator

The generator writes exactly what the brief asks for and copies its framing. So the brief carries the teaching:

- **For each point, give the why, the exact example and the contrast.** Example: "`sorted(nums)` returns a new list and leaves `nums` alone, while `nums.sort()` changes `nums` and returns `None`. The common mistake is `nums = nums.sort()`, which leaves `nums` as `None`."
- **Say who the learner is** and what they already know from earlier lessons.
- **Never name the source** in the brief. When briefs named it, 43 of 59 lessons cited instead of teaching.
- **State facts, never corrections.** "Correction: the book says X" produces a lesson that teaches X.
- **Keep it to 5 to 8 points.** Longer briefs and bare links lose material. One lesson built from a link covered 10 of 40 points.
- **Verify every claim before you send it.** A wrong line in the brief becomes a wrong lesson.
- **Say when a claim applies.** The generator turns one example into a rule unless the brief says where the rule stops.

## Checking the result

- **Read every lesson in full,** with a reviewer who did not write the brief, against `courses/REVIEW_GUIDE.md`.
- **Judge it as a learner.** Could someone who has only this course follow every page and answer every question? Does it teach, or just state?
- **Fix by replacing.** Lessons can't be edited. Fix the brief, generate a replacement, review the replacement too, then delete the old copy.
- **Say what you checked.** "Correct" is not "teaches". Call a lesson fixed only after its replacement passes review.
