# Evals

Two evals, run with `claude -p` (Claude Code's non-interactive mode).

## Triggering

Does Claude load the skill on the right requests and stay out of near-misses? 20 prompts in `triggering_cases.json` (10 should trigger, 10 should not), each run in an empty temp folder with no MCP servers and every tool except Skill disabled. Graded automatically: was the Skill tool called with this skill's name?

```bash
python3 -I evals/run_triggering.py 2
```

## Lesson quality (A/B)

Do the new teaching briefs make better lessons than the old fact-only briefs? 10 passages in `workspace/sources/passages.txt` (10 subjects), one lesson each, built twice from the same points: `eval_old` uses the old preamble, `eval_new` the current `TEACH`. An Opus judge with no tools scores each lesson against `QUALITY_RUBRIC.md` and compares each pair blind, in random order.

From `evals/workspace`, with a Wondering token:

```bash
python3 -I ../../scripts/course_build.py create eval_old
python3 -I ../../scripts/course_build.py create eval_new
# generate all 20 lessons in Chrome (see SKILL.md step 3), then:
python3 -I ../../scripts/course_build.py dump eval_old
python3 -I ../../scripts/course_build.py dump eval_new
python3 -I ../judge_quality.py 2
```

It uses 20 of Wondering's 100 daily generations. Delete both eval courses afterwards.

Results of each run are in `out/` and in `RESULTS.md`.
