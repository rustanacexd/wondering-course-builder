# Write courses/<spec>_deletion_plan.md: every lesson a replacement superseded, for the owner to approve deleting.
#   python -I deletion_plan.py <spec>
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = sys.argv[1]
ids = json.load(open(os.path.join(HERE, "courses", f"{spec}_ids.json"), encoding="utf-8"))
reps = json.load(open(os.path.join(HERE, "courses", f"{spec}_replacements.json"), encoding="utf-8"))
live = {row["lessonId"] for row in ids["lessons"]}
out = ["# Superseded lessons awaiting the owner's approval to delete\n",
       f"Course `{ids['courseId']}`. Each superseded lesson sits right before its replacement, under the same name.",
       "Delete only after the kept lesson passes re-review and the owner approves each `delete_lesson` preview.\n",
       "| n | lesson | delete | kept |", "|---|---|---|---|"]
for r in sorted(reps, key=lambda r: r["n"]):
    kept = ids["lessons"][r["n"] - 1]["lessonId"]
    assert r["old"] not in live and kept in live
    out.append(f"| {r['n']} | {r['name']} | `{r['old']}` | `{kept}` |")
open(os.path.join(HERE, "courses", f"{spec}_deletion_plan.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"{len(reps)} lessons to delete")
