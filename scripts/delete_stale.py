# Delete every lesson in the course that ids.json no longer points at (superseded copies).
#   python -I delete_stale.py <spec> preview   preview each delete_lesson; saves confirm tokens (valid 15 min) to scratch/
#   python -I delete_stale.py <spec> confirm   only after the owner approved the printed previews in chat
import json, os, sys
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)
from lessonlib import HERE
from wondering import call
spec, mode = sys.argv[1], sys.argv[2]
ids = json.load(open(os.path.join(HERE, "courses", f"{spec}_ids.json"), encoding="utf-8"))
os.makedirs(os.path.join(HERE, "scratch"), exist_ok=True)
tok_path = os.path.join(HERE, "scratch", f"{spec}_delete_tokens.json")
live = {r["lessonId"] for r in ids["lessons"]}
course = call("get_course", {"courseId": ids["courseId"]})
present = [(l["id"], l["name"]) for s in course["sections"] for l in s["lessons"]]
assert live <= {i for i, _ in present}, "a live lesson is missing from the course"
stale = [(i, n) for i, n in present if i not in live]

if mode == "preview":
    toks = {}
    for i, n in stale:
        p = call("delete_lesson", {"courseId": ids["courseId"], "lessonId": i})
        toks[i] = p["confirmToken"]
        print(f"{n} | practices {p.get('practiceCount', p.get('preview', {}).get('practiceCount', '?'))} | {p.get('courseName', p.get('preview', {}).get('courseName', ''))}")
    json.dump(toks, open(tok_path, "w"), indent=1)
    print(f"{len(stale)} previews; live lessons kept: {len(live)}")
elif mode == "confirm":
    toks = json.load(open(tok_path))
    done = 0
    for i, n in stale:
        if i in toks:
            call("delete_lesson", {"courseId": ids["courseId"], "lessonId": i, "confirmToken": toks[i]}); done += 1
    os.remove(tok_path)
    left = [l for s in call("get_course", {"courseId": ids["courseId"]})["sections"] for l in s["lessons"]]
    print(f"deleted {done}; course now has {len(left)} lessons; all live present: {live == {l['id'] for l in left}}")
