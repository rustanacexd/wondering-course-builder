# Shared pieces for turning a source (article, book chapter) into Wondering lessons and checking them.
# A plan is plans/<name>.py with URL and LESSONS = [dict(name, section, points, checks=[(label, regex)])].
# Optional per-lesson keys: url (overrides URL), course_section (section title in a new course),
# description (a ready-made brief; then points are not used).
import importlib, os, re, sys
HERE = os.path.abspath(os.environ.get("WONDERING_WORKSPACE", os.getcwd()))  # folder with plans/, courses/, sources/
if HERE not in sys.path:
    sys.path.insert(0, HERE)

def load_plan(name):
    return importlib.import_module(f"plans.{name}")

def brief(url, L):
    try: from guards import GUARDS  # optional guards.py in the workspace
    except ImportError: GUARDS = {}
    g = [GUARDS[L["name"]]] if L["name"] in GUARDS else []
    if L.get("description"):
        return "\n- ".join([L["description"]] + g)
    return TEACH + "Must cover every point below:\n- " + "\n- ".join(L["points"] + g)

# Lessons must teach, not cite: a brief that names its source makes the generator write "from the course" or "the book says".
TEACH = ("Teach each point below directly, as if this lesson is all the learner has. For each idea: say what problem it solves, "
         "show a small concrete example before the general rule, explain every term in plain words the first time it appears, "
         "and show where it stops working or the common mistake. Every code block or list gets a sentence on what it shows. "
         "Never refer to a book, article, author, source, course or chapter (no 'from the course', 'the book says'): explain "
         "the idea yourself. Practice questions make the learner predict a result, spot a mistake or choose between options; "
         "wrong choices are real misconceptions, each explained; each question has exactly one correct answer. ")
SOURCE_REF = re.compile(r"(?i)\b(?:(?:the|this|our|that)\s+(?:book|article|author|course|chapter|tutorial)|(?:book|article|author|course)'s|from the (?:book|article|course|source))\b")

def source_refs(text):
    return [m.group(0) for m in SOURCE_REF.finditer(text)]

def lesson_text(d):
    parts = [d.get("name", "")]
    for p in d.get("pages", []): parts += [p.get("heading", ""), p.get("content", "")]
    for k in d.get("keywords", []): parts += [k.get("name", ""), k.get("description", "")]
    for q in d.get("practices", []):
        parts += [q.get("question", ""), q.get("answer", ""), q.get("explanation", "")]
        parts += [c.get("text", "") for c in (q.get("options") or {}).get("choices", [])]
    return "\n".join(parts).replace('\\"', '"').replace("\\u0027", "'")

def source_text(path):
    # Markdown escapes (\| \{ \< ...) never appear in generated lessons, so drop them before matching.
    return re.sub(r"\\([|{}<>\[\]_*`])", r"\1", open(path, encoding="utf-8").read())

def score(text, checks):
    return [(lbl, bool(re.search(rx, text))) for lbl, rx in checks]

def show(title, hits, verbose=True):
    print(f"\n== {title}  {sum(h for _, h in hits)}/{len(hits)}")
    if verbose:
        for lbl, h in hits: print(("   ok   " if h else "   MISS ") + lbl)

def lint(plan):
    errs = []
    for L in plan.LESSONS:
        n, pts, chk = L["name"], L.get("points", []), L["checks"]
        b = brief(plan.URL, L)
        if not L.get("description") and not 4 <= len(pts) <= 8: errs.append(f"{n}: {len(pts)} points (want 4-8)")
        if not 5 <= len(chk) <= 12: errs.append(f"{n}: {len(chk)} checks (want 5-12)")
        if len(b) > 2400: errs.append(f"{n}: brief is {len(b)} chars (max 2400)")
        if source_refs(b.replace(TEACH, "")): errs.append(f"{n}: brief refers to its source: {source_refs(b.replace(TEACH, ''))}")
        if len(n) > 70: errs.append(f"{n}: name longer than 70 chars")
        for lbl, rx in chk:
            try: re.compile(rx)
            except re.error as e: errs.append(f"{n}: bad regex for {lbl!r}: {e}")
    names = [L["name"] for L in plan.LESSONS]
    errs += [f"duplicate lesson name {x!r}" for x in set(names) if names.count(x) > 1]
    return errs

def selftest(plan, good_paths, bad_paths, max_bad=1):
    """Checks must all match the source and match at most max_bad times per lesson on unrelated text."""
    good = "\n".join(source_text(p) for p in good_paths)
    errs = lint(plan)
    for L in plan.LESSONS:
        hits = score(good, L["checks"])
        show(f"[source] {L['name']}", hits, verbose=False)
        errs += [f"{L['name']}: check {lbl!r} does not match the source" for lbl, h in hits if not h]
    for bp in bad_paths:
        bad = source_text(bp)
        for L in plan.LESSONS:
            hits = [lbl for lbl, h in score(bad, L["checks"]) if h]
            if len(hits) > max_bad:
                errs.append(f"{L['name']}: {len(hits)} checks match unrelated text {os.path.basename(bp)}: {hits}")
    print("\nSELFTEST " + ("PASS" if not errs else "FAIL"))
    for e in errs: print("  - " + e)
    return not errs
