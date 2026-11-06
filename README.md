# wondering-course-builder

A Claude Code skill that turns articles, docs and book chapters into [Wondering](https://wondering.app) courses through the Wondering MCP, and checks that every lesson actually teaches.

Wondering writes each lesson from a short brief, and most bad lessons trace back to that brief. A brief that only lists facts gets a lesson that lists facts. A brief that names its source gets a lesson that says "from the book" instead of explaining. This skill writes briefs that ask for teaching, checks what Wondering generated, and replaces any lesson that fails.

**Read [GUIDELINES.md](GUIDELINES.md)** for what makes a good lesson and how to get one from a generator.

## Install

```bash
git clone https://github.com/rustanacexd/wondering-course-builder ~/.claude/skills/wondering-course-builder
```

Claude Code then offers `/wondering-course-builder` in every project and loads it when you ask for a Wondering course.

You also need:

- Python 3.9+. Only the standard library is used.
- A Wondering account with MCP access. Create a token under Settings, then API Access, and save it to `~/.wondering-setup/token` (or set `WONDERING_TOKEN_FILE`). Never commit it.
- Claude in Chrome, to open each lesson so Wondering generates it.

## Use

Make a folder for your course and ask Claude, for example: "build a Wondering course from these three articles". The skill plans the lessons, creates the course, generates every lesson in Chrome, then checks and reviews them. It replaces the lessons that fail and deletes the old copies once you approve.

To see the shape of a course without touching Wondering:

```bash
cd ~/.claude/skills/wondering-course-builder/example
python3 -I ../scripts/course_build.py selftest example
python3 -I ../scripts/course_build.py preview example
```

`preview` writes `courses/example_outline.md`, with each brief exactly as Wondering will receive it.

## Layout

| Path | What it is |
|---|---|
| `SKILL.md` | The steps Claude follows |
| `GUIDELINES.md` | What a good course, lesson and quiz look like, and how to brief for them |
| `REVIEW_GUIDE.md` | The bar a reviewer uses to pass or fail a lesson |
| `scripts/lessonlib.py` | Brief preamble (`TEACH`), lint, coverage checks |
| `scripts/course_build.py` | `selftest`, `preview`, `create`, `check`, `dump` |
| `scripts/article_lessons.py` | Add one source's lessons to an existing course |
| `scripts/replace_lessons.py` | Insert a corrected replacement after a lesson |
| `scripts/refresh_lessons.py` | Wait for generation, then dump the lessons |
| `scripts/delete_stale.py` | Delete superseded copies, then check the live lessons |
| `scripts/generate_click.js` | Browser script that starts generating one lesson |
| `scripts/wondering.py` | Minimal Wondering MCP client |
| `example/` | A one-lesson example workspace: plan, spec, sources, `guards.py` |

## Limits

- No tool edits a lesson after it is generated. Fixing a lesson means replacing it.
- Wondering generates at most 100 lessons a day, and replacements count.
- Delete previews expire after 15 minutes.
