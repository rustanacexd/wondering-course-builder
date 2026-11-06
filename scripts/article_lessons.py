# Turn one article into several Wondering lessons and verify what Wondering generated.
#   python -I article_lessons.py selftest <plan> <source.txt> [<known-bad.txt>]  checks must all pass on the source
#   python -I article_lessons.py insert   <plan> <afterLessonId>                 inserts lessons in order, saves IDs
#   python -I article_lessons.py check    <plan>                                 per-lesson coverage of generated lessons
# For a whole new course built from several plans, use course_build.py.
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # python -I drops the script's folder
from lessonlib import HERE, brief, lesson_text, load_plan, score, selftest, show
COURSE = os.environ.get("WONDERING_COURSE_ID")  # the course to insert into

cmd, plan_name = sys.argv[1], sys.argv[2]
plan = load_plan(plan_name)
ids_file = os.path.join(HERE, "plans", f"{plan_name}_created.json")

if cmd == "selftest":
    sys.exit(0 if selftest(plan, [sys.argv[3]], sys.argv[4:]) else 1)

elif cmd == "insert":
    from wondering import call
    after, ids = sys.argv[3], []
    for L in plan.LESSONS:
        r = call("insert_lesson", {"courseId": COURSE, "name": L["name"], "description": brief(plan.URL, L), "afterLessonId": after})
        print(r["status"], r["lessonId"], L["name"]); ids.append(r["lessonId"]); after = r["lessonId"]
    json.dump(ids, open(ids_file, "w"))

elif cmd == "check":
    from wondering import call
    tot = [0, 0]
    for L, lid in zip(plan.LESSONS, json.load(open(ids_file))):
        d = call("get_lesson", {"lessonId": lid, "includePractices": True})
        if not d["pages"]: print(f"\n== {L['name']}  NOT GENERATED YET"); continue
        hits = score(lesson_text(d), L["checks"]); show(f"{L['name']}  ({len(d['pages'])} pages)", hits)
        tot[0] += sum(h for _, h in hits); tot[1] += len(hits)
    print(f"\nTOTAL {tot[0]}/{tot[1]}")
