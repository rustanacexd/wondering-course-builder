# Build a whole new Wondering course from several plans, then verify what Wondering generated.
#   python -I course_build.py selftest <spec>   every plan's checks: match its source, rarely match unrelated text
#   python -I course_build.py preview  <spec>   writes courses/<spec>_outline.md and _payload.json; no network
#   python -I course_build.py create   <spec>   one create_course call; saves lesson IDs (refuses if already created)
#   python -I course_build.py check    <spec>   per-lesson coverage of generated lessons -> courses/<spec>_check.json
#   python -I course_build.py dump     <spec>   generated lesson text -> courses/<spec>_lessons/NN_name.md
# A spec is courses/<spec>.py with NAME, GOAL and PARTS = [dict(plan, source, bad=[...], section=None)].
# A lesson's course section is its course_section, else its part's section.
import importlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I drops the script's folder
from lessonlib import HERE, brief, lesson_text, lint, load_plan, score, selftest, show, source_refs

def lessons(spec):
    """Flattened course order: (section title, plan name, plan, lesson dict)."""
    out = []
    for part in spec.PARTS:
        plan = load_plan(part["plan"])
        for L in plan.LESSONS:
            sec = L.get("course_section") or part.get("section")
            if not sec: raise SystemExit(f"{part['plan']}: lesson {L['name']!r} has no section")
            out.append((sec, part["plan"], plan, L))
    return out

def payload(spec):
    sections = []
    for sec, _, plan, L in lessons(spec):
        if not sections or sections[-1]["name"] != sec:
            sections.append({"name": sec, "lessons": []})
        sections[-1]["lessons"].append({"name": L["name"], "description": brief(plan.URL, L)})
    titles = [s["name"] for s in sections]
    dup = sorted({t for t in titles if titles.count(t) > 1})
    if dup: raise SystemExit(f"section titles split by other sections: {dup}")
    return {"name": spec.NAME, "goal": spec.GOAL, "sections": sections}

def path(spec_name, suffix):
    return os.path.join(HERE, "courses", f"{spec_name}{suffix}")

spec_name = sys.argv[2]
spec = importlib.import_module(f"courses.{spec_name}")
cmd = sys.argv[1]

if cmd == "selftest":
    bad = []
    for part in spec.PARTS:
        print(f"\n######## {part['plan']}")
        if not selftest(load_plan(part["plan"]), [os.path.join(HERE, part["source"])],
                        [os.path.join(HERE, b) for b in part["bad"]]):
            bad.append(part["plan"])
    names = [L["name"] for _, _, _, L in lessons(spec)]
    dups = sorted({n for n in names if names.count(n) > 1})
    if dups: bad.append(f"duplicate lesson names across plans: {dups}")
    print("\nCOURSE SELFTEST " + ("PASS" if not bad else f"FAIL: {bad}"))
    sys.exit(1 if bad else 0)

elif cmd == "preview":
    p = payload(spec)
    json.dump(p, open(path(spec_name, "_payload.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n, md = 0, [f"# {p['name']}\n", f"Goal: {p['goal']}\n"]
    for s in p["sections"]:
        md.append(f"\n## {s['name']} ({len(s['lessons'])} lessons)\n")
        for l in s["lessons"]:
            n += 1
            md.append(f"\n### {n}. {l['name']}\n\n```txt\n{l['description']}\n```\n")
    open(path(spec_name, "_outline.md"), "w", encoding="utf-8").write("".join(md))
    for s in p["sections"]:
        print(f"{s['name']}: {len(s['lessons'])}")
    print(f"TOTAL {n} lessons in {len(p['sections'])} sections; payload {len(json.dumps(p))} bytes; "
          f"longest brief {max(len(l['description']) for s in p['sections'] for l in s['lessons'])} chars")

elif cmd == "create":
    from wondering import call
    ids_path = path(spec_name, "_ids.json")
    if os.path.exists(ids_path): raise SystemExit(f"already created: {ids_path}")
    p = payload(spec)
    try:
        r = call("create_course", p)
    except Exception as e:  # the course may exist anyway; never retry blindly
        same = [c for c in call("get_learning_summary", {"limit": 1})["activeCourses"] if c.get("name") == p["name"]]
        raise SystemExit(f"create_course failed: {e!r}. Courses already named {p['name']!r}: {same}")
    json.dump(r, open(path(spec_name, "_create_response.json"), "w"), indent=1)
    course_id = r["courseId"]
    c = call("get_course", {"courseId": course_id})
    got = [(s["name"], l["name"], l["id"]) for s in c["sections"] for l in s["lessons"]]
    want = [(sec, L["name"], plan_name) for sec, plan_name, _, L in lessons(spec)]
    rows = []
    for i, (sec, name, plan_name) in enumerate(want):
        match = got[i] if i < len(got) and got[i][1] == name else next((g for g in got if g[1] == name), None)
        rows.append({"section": sec, "plan": plan_name, "name": name, "lessonId": match[2] if match else None})
    json.dump({"courseId": course_id, "lessons": rows}, open(ids_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    missing = [r["name"] for r in rows if not r["lessonId"]]
    print(f"courseId {course_id}: {len(got)} lessons in Wondering, {len(want)} planned, {len(missing)} unmatched")
    for m in missing: print("  UNMATCHED", m)

elif cmd in ("check", "dump"):
    from wondering import call
    ids = json.load(open(path(spec_name, "_ids.json"), encoding="utf-8"))
    by_name = {L["name"]: L for _, _, _, L in lessons(spec)}
    report, tot, pending, srcref = [], [0, 0], [], []
    os.makedirs(path(spec_name, "_lessons"), exist_ok=True)
    for i, row in enumerate(ids["lessons"], 1):
        d = call("get_lesson", {"lessonId": row["lessonId"], "includePractices": True})
        if not d.get("pages"):
            pending.append(row["name"]); report.append({**row, "generated": False}); continue
        text = lesson_text(d)
        if cmd == "dump":
            slug = re.sub(r"[^a-z0-9]+", "-", row["name"].lower()).strip("-")[:50]
            open(os.path.join(path(spec_name, "_lessons"), f"{i:02d}_{slug}.md"), "w", encoding="utf-8").write(
                json.dumps(d, ensure_ascii=False, indent=1))
            continue
        hits = score(text, by_name[row["name"]]["checks"])
        refs = source_refs(text)
        srcref.extend([i] if refs else [])
        show(f"{i:02d}. {row['name']}  ({len(d['pages'])} pages)" + (f"  SOURCE REFS {len(refs)}: {refs[:4]}" if refs else ""), hits)
        tot[0] += sum(h for _, h in hits); tot[1] += len(hits)
        report.append({**row, "generated": True, "pages": len(d["pages"]),
                       "covered": sum(h for _, h in hits), "total": len(hits),
                       "misses": [lbl for lbl, h in hits if not h]})
    if cmd == "check":
        json.dump(report, open(path(spec_name, "_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\nTOTAL {tot[0]}/{tot[1]} over {len(ids['lessons']) - len(pending)} generated lessons; {len(pending)} not generated yet")
        print(f"SOURCE REFS in {len(srcref)} lessons: {srcref}")
    else:
        print(f"dumped {len(ids['lessons']) - len(pending)} generated lessons; {len(pending)} not generated yet")
