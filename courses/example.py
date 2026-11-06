# Example course spec: NAME, GOAL and PARTS. Each part is one plan, its source, and unrelated text the checks must not match.
NAME = "Example: Python lists"
GOAL = "Index, slice, change and sort Python lists."
PARTS = [
    dict(plan="example", source="sources/example.txt", bad=["sources/unrelated.txt"], section="Python lists"),
]
