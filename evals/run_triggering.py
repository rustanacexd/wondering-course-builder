# Triggering eval: does Claude Code load the skill on the right requests and not on near-misses?
#   python3 -I evals/run_triggering.py [reps] [--only=p01,n08]   (default 2 reps; writes evals/out/triggering.json)
# Each case runs in a fresh, empty temp folder with `claude -p`, no MCP servers, and every tool except Skill
# disallowed, so nothing outside the run can change. Graded programmatically: was the Skill tool called
# with this skill's name?
import json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = "wondering-course-builder"
args = [a for a in sys.argv[1:] if not a.startswith("--only=")]
only = next((a[7:].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
reps = int(args[0]) if args else 2
cases = [c for c in json.load(open(os.path.join(HERE, "triggering_cases.json"), encoding="utf-8")) if not only or c["id"] in only]
BLOCK = "Bash Edit Write NotebookEdit WebFetch WebSearch Agent Read Glob Grep TodoWrite"

def run(case_rep):
    case, rep = case_rep
    with tempfile.TemporaryDirectory() as d:
        t0 = time.time()
        p = subprocess.run(["claude", "-p", case["prompt"], "--output-format", "stream-json", "--verbose",
                            "--max-turns", "2", "--strict-mcp-config", "--allowedTools", "Skill",
                            "--disallowedTools", BLOCK],
                           cwd=d, capture_output=True, text=True, encoding="utf-8", timeout=300)
    skills, model = [], None
    for line in p.stdout.splitlines():
        try: ev = json.loads(line)
        except ValueError: continue
        if ev.get("type") == "system" and ev.get("model"): model = ev["model"]
        for b in (ev.get("message") or {}).get("content") or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Skill":
                skills.append((b.get("input") or {}).get("skill"))
    fired = any(s and s.split(":")[-1] == SKILL for s in skills)
    return {"id": case["id"], "rep": rep, "expect": case["expect"], "fired": fired, "skills": skills,
            "model": model, "secs": round(time.time() - t0, 1),
            "exit": 0 if fired else p.returncode,  # a fired skill then hits the 2-turn cap by design
            "stderr": p.stderr[-300:] if p.returncode and not fired else ""}

jobs = [(c, r) for c in cases for r in range(reps)]
with ThreadPoolExecutor(4) as ex: res = list(ex.map(run, jobs))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "out", "triggering_smoke.json" if only else "triggering.json"), "w", encoding="utf-8"), indent=1)

tp = sum(r["fired"] and r["expect"] for r in res); fn = sum(not r["fired"] and r["expect"] for r in res)
fp = sum(r["fired"] and not r["expect"] for r in res); tn = sum(not r["fired"] and not r["expect"] for r in res)
errs = [f"{r['id']}#{r['rep']}" for r in res if r["exit"]]
print(f"runs {len(res)}  model {res[0]['model']}  errors {errs or 'none'}")
print(f"recall (fires when it should)   {tp}/{tp + fn}")
print(f"specificity (quiet when it should be) {tn}/{tn + fp}")
for r in res:
    if r["fired"] != r["expect"]:
        print(f"  MISS {r['id']}#{r['rep']} expect={r['expect']} skills={r['skills']}")
