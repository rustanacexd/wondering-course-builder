---
name: wondering-course-builder
description: Create, generate, check, review, fix or delete Wondering lessons and courses through the Wondering MCP, from an article, docs page or book chapter. Use when asked to make a Wondering course or lessons, generate lessons in the browser, replace a bad lesson, check that lessons teach instead of citing their source, or delete old copies.
---

# Wondering course builder

Paths are relative to the repo root. Use `python3 -I`. Read `GUIDELINES.md` before writing any brief: it says what a good lesson is, and the brief is the only lever.

A course has a spec `courses/<spec>.py`, plans in `plans/`, and sources in `sources/`. After creation, the live lesson IDs are in `courses/<spec>_ids.json` and the replacements in `courses/<spec>_replacements.json`. The example spec is `example`.

## Rules

- Delete superseded copies and old courses once their replacements pass review. Never leave them in the course.
- Never send `submit_feedback` unless the owner asks.
- Generate lessons yourself in the browser. The owner never has to click.
- Never print the token. The token file is `$WONDERING_TOKEN_FILE`, default `~/.wondering-setup/token`. Reviewers (subagents) never read it: give them dumped files.

## Plan and check offline

```bash
python3 -I course_build.py selftest example    # every check matches its source and not the unrelated text
python3 -I course_build.py preview example     # writes courses/example_outline.md and _payload.json
```

## Create, generate, verify

1. Create the course in one call: `python3 -I course_build.py create example`. Or add lessons to an existing course: `WONDERING_COURSE_ID=<id> python3 -I article_lessons.py insert <plan> <afterLessonId>`.
2. Generate each lesson in Chrome (Claude in Chrome). Per lesson, `navigate` to `https://wondering.app/?project=<courseId>`, then run `.claude/skills/wondering-course-builder/generate_click.js` with `javascript_tool`, with `__SID__` replaced by the lesson's `sessionId`. It must return `CREATING`. Navigate again before every lesson.
3. Check coverage and citations: `python3 -I course_build.py check example`. Every lesson needs full coverage and no `SOURCE REFS`.
4. Dump for review: `python3 -I course_build.py dump example`.
5. Review every lesson with an independent subagent, against `courses/REVIEW_GUIDE.md` and `GUIDELINES.md`. The reviewer checks every claim and every quiz choice and judges the lesson as a learner would.

## Fix a lesson

No tool edits a lesson. Fix the brief (or add a verified note to `guards.py`), then:

```bash
python3 -I replace_lessons.py example 3          # insert a replacement after lesson 3 (--again replaces a replacement)
python3 -I refresh_lessons.py example            # after generating it in Chrome: wait, dump, flatten
```

Review the replacement like a new lesson. Then delete the old copies:

```bash
python3 -I delete_stale.py example preview       # show these lines to the owner
python3 -I delete_stale.py example confirm       # after their go; tokens expire in 15 minutes
```

## Gotchas

- Lessons stay empty until opened in the app. Done means `get_lesson` shows pages and practices. If a lesson has pages but no quiz, click "Start reading" again.
- A script looping over lessons on one page breaks after a click opens a lesson. Navigate before every click.
- Daily cap: 100 generations, reset at local midnight, and replacements count. At the cap the click fails silently. Only `LIMIT` shows it.
- Delete tokens last 15 minutes. If the owner approves later, fetch fresh previews and confirm in one run, but only when the lesson IDs match the approved set.
- Unknown tool arguments are ignored without an error. Take argument names from the live `tools/list`.
