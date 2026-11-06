# Lesson-quality A/B judge. Run from evals/workspace after both courses are generated and dumped:
#   python3 -I ../../scripts/course_build.py dump eval_old && python3 -I ../../scripts/course_build.py dump eval_new
#   python3 -I ../judge_quality.py [reps]      (default 1; writes ../out/quality.json and prints the summary)
# The judge is `claude -p --model opus` with every tool disabled: it only reads the lesson text it is given.
# Pairwise order is randomized per pair so position bias cancels out.
import glob, json, os, random, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); WS = os.getcwd()
reps = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rubric = open(os.path.join(HERE, "QUALITY_RUBRIC.md"), encoding="utf-8").read()
ABS, PAIR = rubric.split("# Pairwise (judge)")
BLOCK = "Bash Edit Write NotebookEdit WebFetch WebSearch Agent Read Glob Grep TodoWrite Skill"

sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from lessonlib import lesson_text

def lessons(spec):  # flattened text: pages, widgets, keywords, practices with choices, answer and explanation
    return {int(os.path.basename(f)[:2]): lesson_text(json.load(open(f, encoding="utf-8")))
            for f in sorted(glob.glob(os.path.join(WS, "courses", f"{spec}_lessons", "*.md")))}

def ask(prompt):  # prompt goes on stdin: lessons are too long for a command line
    p = subprocess.run(["claude", "-p", "--model", "opus", "--max-turns", "1", "--strict-mcp-config",
                        "--disallowedTools", BLOCK], input=prompt, capture_output=True, text=True,
                       encoding="utf-8", timeout=600)
    m = re.search(r"\{.*\}", p.stdout, re.S)
    return json.loads(m.group(0)) if m else {"error": p.stdout[-300:] or p.stderr[-300:]}

A, B = lessons("eval_old"), lessons("eval_new")
ns = sorted(set(A) & set(B))
jobs = []
for r in range(reps):
    for n in ns:
        jobs.append(("abs", "old", n, r, ABS + "\n\nLESSON:\n" + A[n]))
        jobs.append(("abs", "new", n, r, ABS + "\n\nLESSON:\n" + B[n]))
        flip = random.Random(f"{n}-{r}").random() < 0.5
        x, y = (B[n], A[n]) if flip else (A[n], B[n])
        jobs.append(("pair", "new=X" if flip else "new=Y", n, r, PAIR + "\n\nLESSON X:\n" + x + "\n\nLESSON Y:\n" + y))
with ThreadPoolExecutor(4) as ex: outs = list(ex.map(lambda j: ask(j[4]), jobs))
res = [{"kind": k, "arm": a, "n": n, "rep": r, "out": o} for (k, a, n, r, _), o in zip(jobs, outs)]
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
json.dump(res, open(os.path.join(HERE, "out", "quality.json"), "w", encoding="utf-8"), indent=1)

keys = ["problem", "example_first", "plain_terms", "limits", "explains_examples", "thinking_quiz",
        "misconception_distractors", "overall", "cites_source", "bad_quizzes", "false_claims"]
def mean(arm, k):
    v = [x["out"][k] for x in res if x["kind"] == "abs" and x["arm"] == arm and isinstance(x["out"].get(k), (int, float))]
    return round(sum(v) / len(v), 2) if v else None
print(f"lessons {len(ns)} x reps {reps}; judge errors {sum('error' in x['out'] for x in res)}")
print(f"{'':28}{'old':>6}{'new':>6}")
for k in keys: print(f"{k:28}{mean('old', k)!s:>6}{mean('new', k)!s:>6}")
wins = {"new": 0, "old": 0, "tie": 0}
for x in res:
    if x["kind"] != "pair" or "better" not in x["out"]: continue
    b = x["out"]["better"]; new_is = x["arm"][-1]
    wins["tie" if b == "tie" else ("new" if b == new_is else "old")] += 1
print(f"pairwise: new better {wins['new']}, old better {wins['old']}, tie {wins['tie']}")
