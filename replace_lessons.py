# Insert a corrected copy of a lesson right after the original (same name, brief rebuilt from the fixed plan).
# The original stays until the owner approves deleting it; ids.json then points at the replacement.
#   python -I replace_lessons.py <spec> 13 14 16 ...   (course positions, 1-based; already replaced ones are skipped)
#   python -I replace_lessons.py <spec> --again 26     (replace a replacement that failed re-review)
# The replacements file is the record of every superseded lesson (old -> new, in order).
import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lessonlib import HERE, brief, lint, load_plan
from wondering import call

spec_name, again = sys.argv[1], "--again" in sys.argv[2:]
positions = [int(a) for a in sys.argv[2:] if a != "--again"]
spec = importlib.import_module(f"courses.{spec_name}")
ids_path = os.path.join(HERE, "courses", f"{spec_name}_ids.json")
rep_path = os.path.join(HERE, "courses", f"{spec_name}_replacements.json")
ids = json.load(open(ids_path, encoding="utf-8"))
reps = json.load(open(rep_path, encoding="utf-8")) if os.path.exists(rep_path) else []

for n in positions:
    row = ids["lessons"][n - 1]
    if any(r["new"] == row["lessonId"] for r in reps) != again:
        print(f"{n:02d} skip: {'already replaced' if not again else 'not a replacement yet'}"); continue
    plan = load_plan(row["plan"])
    errs = [e for e in lint(plan) if e.startswith(row["name"] + ":")]
    if errs: sys.exit(f"{n:02d} not inserted, brief fails lint: {errs}")
    L = next(L for L in plan.LESSONS if L["name"] == row["name"])
    desc = brief(getattr(plan, "URL", ""), L)
    r = call("insert_lesson", {"courseId": ids["courseId"], "name": row["name"], "description": desc,
                               "afterLessonId": row["lessonId"]})
    reps.append({"n": n, "name": row["name"], "old": row["lessonId"], "new": r["lessonId"],
                 "sessionId": r.get("sessionId"), "briefChars": len(desc)})
    row["lessonId"] = r["lessonId"]
    json.dump(reps, open(rep_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ids, open(ids_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{n:02d} inserted {r['lessonId']} after {reps[-1]['old']}  {row['name']}")
