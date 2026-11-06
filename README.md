# wondering-course-builder

Turn an article, docs page or book chapter into [Wondering](https://wondering.app) lessons through the Wondering MCP, and check that the lessons actually teach.

Wondering writes each lesson from a short brief. Most bad lessons trace back to the brief. A brief that lists facts gets a lesson that lists facts. A brief that names its source gets a lesson that says "from the book" instead of explaining. This repo builds briefs that ask for teaching, checks what Wondering generated, and replaces lessons that fail.

**Start with [GUIDELINES.md](GUIDELINES.md):** what makes a good lesson, and how to get one from a generator.

## What's here

| File | What it does |
|---|---|
| `GUIDELINES.md` | What a good course, lesson and quiz look like, and how to brief for them |
| `courses/REVIEW_GUIDE.md` | The bar a reviewer uses to pass or fail a lesson |
| `lessonlib.py` | Brief template (`TEACH`), lint, coverage checks |
| `course_build.py` | `selftest`, `preview`, `create`, `check`, `dump` for a course spec |
| `article_lessons.py` | The same for adding one article's lessons to an existing course |
| `replace_lessons.py` | Insert a corrected replacement after a lesson |
| `refresh_lessons.py` | Wait for generation, dump and flatten the lessons |
| `delete_stale.py` | Delete every superseded copy, then check the live set |
| `guards.py` | Verified correction notes, per lesson, appended to its brief |
| `wondering.py` | Minimal Wondering MCP client over HTTP |
| `plans/`, `courses/`, `sources/` | An example plan, course spec and source |
| `.claude/skills/wondering-course-builder/` | A Claude Code skill that runs the whole flow, plus the browser script that starts generation |

## Setup

Requires Python 3.9+ (standard library only) and a Wondering account with MCP access. Works on macOS and Linux.

1. Create a token in Wondering: Settings, then API Access.
2. Save it to `~/.wondering-setup/token`, or point `WONDERING_TOKEN_FILE` at another file. Never commit it.
3. Try the offline steps:

```bash
python3 -I course_build.py selftest example
python3 -I course_build.py preview example
```

`preview` writes the full outline to `courses/example_outline.md`, with every brief exactly as Wondering will receive it.

## Flow

1. **Plan.** For each source, write `plans/<name>.py`: lessons of 5 to 8 points each, plus one regex check per point. Each point carries the idea, an exact example, and where it stops working. See `GUIDELINES.md`.
2. **Self-test.** Every check must match the source and almost never match unrelated text.
3. **Create** the course (`course_build.py create <spec>`) or insert lessons into an existing one (`article_lessons.py insert`).
4. **Generate.** Wondering only writes a lesson when it is opened in the app. The skill opens each one in Chrome with `generate_click.js`.
5. **Check** coverage and citations (`course_build.py check <spec>`), then **review** every lesson against `courses/REVIEW_GUIDE.md`.
6. **Fix** each failure with a replacement (`replace_lessons.py`), review it again, then **delete** the old copies (`delete_stale.py`).

## Limits worth knowing

- No tool edits a lesson after generation. Fixing means replacing.
- Wondering generates at most 100 lessons a day, and replacements count.
- Delete previews expire after 15 minutes.
