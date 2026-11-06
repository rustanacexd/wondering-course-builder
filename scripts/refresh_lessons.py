# Wait until every live replacement has pages and practices, then dump all lessons and rewrite the flattened text.
#   python -I refresh_lessons.py <spec>        (then: python -I course_build.py check <spec>)
import glob, json, os, subprocess, sys, time
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
SCRIPTS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPTS)
from lessonlib import HERE
from lessonlib import lesson_text
from wondering import call

spec = sys.argv[1]
ids = json.load(open(os.path.join(HERE, "courses", f"{spec}_ids.json"), encoding="utf-8"))
live = {(n + 1, row["lessonId"]) for n, row in enumerate(ids["lessons"])}
reps = json.load(open(os.path.join(HERE, "courses", f"{spec}_replacements.json"), encoding="utf-8"))
wanted = sorted({(r["n"], r["new"]) for r in reps} & live)

def ready(item):  # get_lesson is a read, so retrying a 5xx is safe
    for attempt in range(4):
        try:
            d = call("get_lesson", {"lessonId": item[1], "includePractices": True})
            return bool(d.get("pages")) and bool(d.get("practices"))
        except HTTPError as e:
            if e.code < 500 or attempt == 3: raise
            time.sleep(5 * (attempt + 1))

for i in range(60):
    with ThreadPoolExecutor(4) as ex: st = list(ex.map(ready, wanted))
    if all(st): print(f"all {len(wanted)} replacements ready after {i * 10}s"); break
    time.sleep(10)
else:
    print("NOT READY:", [n for (n, _), s in zip(wanted, st) if not s])
subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "course_build.py"), "dump", spec], check=True)
os.makedirs(os.path.join(HERE, "courses", f"{spec}_lessons_txt"), exist_ok=True)
for f in sorted(glob.glob(os.path.join(HERE, "courses", f"{spec}_lessons", "*.md"))):
    d = json.load(open(f, encoding="utf-8"))
    open(os.path.join(HERE, "courses", f"{spec}_lessons_txt", os.path.basename(f)[:-3] + ".txt"), "w", encoding="utf-8").write(lesson_text(d))
print("txt refreshed")
