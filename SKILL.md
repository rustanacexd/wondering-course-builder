---
name: wondering-course-builder
description: Builds Wondering courses and lessons from source material (articles, docs, book chapters) through the Wondering MCP, then checks that every lesson teaches instead of citing its source. Use when asked to create a Wondering course or lessons from a source, generate lessons, fix or replace a bad lesson, review lessons, or delete old lesson copies.
allowed-tools: Bash(python3 -I ${CLAUDE_SKILL_DIR}/scripts/*)
---

# Wondering course builder

Run every command from the workspace: the folder that holds `plans/`, `courses/` and `sources/`. Create it if missing (copy `${CLAUDE_SKILL_DIR}/example/` for the layout). Scripts are in `${CLAUDE_SKILL_DIR}/scripts/` and need only Python 3.

Read [GUIDELINES.md](GUIDELINES.md) before writing any brief. Give [REVIEW_GUIDE.md](REVIEW_GUIDE.md) to every reviewer.

## Rules

- The brief is the only lever. Every brief asks for teaching (problem, example, contrast) and never names its source.
- Verify every claim in a brief before inserting it.
- Generate lessons yourself in the browser. The owner never clicks.
- Review every lesson and every replacement. Report which lessons were checked, and for what.
- Delete superseded copies once their replacements pass. Never leave them in the course.
- Never print the token (`$WONDERING_TOKEN_FILE`, default `~/.wondering-setup/token`). Reviewers never read it.
- Do not send `submit_feedback` unless the owner asks.

## 1. Plan

For each source, write `plans/<name>.py` (shape: `${CLAUDE_SKILL_DIR}/example/plans/example.py`): lessons of 5 to 8 points, one regex check per point. Each point holds the idea, its exact example, and where it stops working. Add a spec `courses/<spec>.py` listing the parts. Then:

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/course_build.py selftest <spec>
python3 -I ${CLAUDE_SKILL_DIR}/scripts/course_build.py preview <spec>
```

Selftest must pass. Show the owner `courses/<spec>_outline.md` and cut what they don't want.

## 2. Create

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/course_build.py create <spec>
```

To add lessons to an existing course instead: `WONDERING_COURSE_ID=<id> python3 -I ${CLAUDE_SKILL_DIR}/scripts/article_lessons.py insert <plan> <afterLessonId>`.

## 3. Generate

Lessons stay empty until opened in the app. For each lesson, with Claude in Chrome:

1. `navigate` to `https://wondering.app/?project=<courseId>`.
2. Run `${CLAUDE_SKILL_DIR}/scripts/generate_click.js` in `javascript_tool`, with `__SID__` replaced by the lesson's `sessionId`.
3. Expect `CREATING`. `LIMIT` means the daily cap (100 a day, resets at local midnight).

Navigate again before every lesson. Several navigate/script pairs can share one `browser_batch`.

## 4. Check and review

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/course_build.py check <spec>
python3 -I ${CLAUDE_SKILL_DIR}/scripts/course_build.py dump <spec>
```

`check` must show full coverage and no `SOURCE REFS` for every lesson. Then give independent reviewers the dumped lessons (`courses/<spec>_lessons/`), the outline and REVIEW_GUIDE.md. They verify every claim and every quiz choice and judge each lesson as a learner would.

## 5. Fix

No tool edits a lesson. Fix the brief, or add a verified note in the workspace's `guards.py` (`GUARDS = {"<lesson name>": "<note>"}`), then insert a replacement and generate it (step 3):

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/replace_lessons.py <spec> <n> [<n> ...]
python3 -I ${CLAUDE_SKILL_DIR}/scripts/refresh_lessons.py <spec>
```

Use `--again` to replace a replacement. Review it like a new lesson.

## 6. Delete old copies

```bash
python3 -I ${CLAUDE_SKILL_DIR}/scripts/delete_stale.py <spec> preview
python3 -I ${CLAUDE_SKILL_DIR}/scripts/delete_stale.py <spec> confirm
```

Show the preview lines with the results and confirm on the owner's go. Tokens expire in 15 minutes. If they have expired, preview and confirm together, but only when the lesson IDs match the approved set. Confirm ends with `all live present: True`.

## Gotchas

- If a lesson has pages but no quiz, click "Start reading" again.
- One script that loops over lessons on a single page breaks after a click opens a lesson. Navigate before every click.
- Unknown tool arguments are ignored silently. Take argument names from the live `tools/list`.
- A replacement can fix one error and add another. Review it again.
