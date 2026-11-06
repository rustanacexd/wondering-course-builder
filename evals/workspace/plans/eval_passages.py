# One lesson per passage in sources/passages.txt. Both eval arms use these exact points; only the brief preamble differs.
URL = "https://example.com/eval-passages"
L = lambda name, points, checks: dict(name=name, section="Eval", points=points, checks=checks)
LESSONS = [
 L("SQL joins: INNER, LEFT and NULL rows", [
   "Tables customers(id, name) and orders(id, customer_id, total). INNER JOIN returns only customers with at least one order.",
   "LEFT JOIN keeps every customer; for a customer with no orders the order columns are NULL.",
   "WHERE orders.total > 10 drops the NULL rows and turns a LEFT JOIN into an inner join; put the condition in ON to keep them.",
   "COUNT(orders.id) gives 0 for a customer with no orders; COUNT(*) gives 1."],
  [("inner join", r"INNER JOIN"), ("left join", r"LEFT JOIN"), ("NULL", r"NULL"), ("filter in ON", r"\bON\b"), ("count star", r"COUNT\(\*\)")]),
 L("Git rebase vs merge", [
   "git merge main adds a merge commit and keeps both histories as they were.",
   "git rebase main replays the feature commits on top of main: new hashes, straight-line history.",
   "Never rebase commits others have already pulled: their copies no longer match.",
   "Rebase conflicts come one commit at a time: fix, git add, then git rebase --continue."],
  [("merge", r"git merge"), ("rebase", r"git rebase main"), ("new hashes", r"(?i)hash"), ("shared commits", r"(?i)pulled|shared|pushed"), ("continue", r"rebase --continue")]),
 L("Compound interest and the rule of 72", [
   "A = P(1 + r/n)^(nt).",
   "$1,000 at 5% compounded yearly for 2 years is $1,102.50; simple interest gives $1,100.",
   "Compounded monthly the same deposit grows to $1,104.94.",
   "Rule of 72: at 6% a year money doubles in about 72 / 6 = 12 years."],
  [("formula", r"\(1 \+ r/n\)"), ("1102.50", r"1,?102\.50"), ("1100", r"1,?100\b"), ("monthly", r"1,?104\.94"), ("rule of 72", r"(?i)rule of 72")]),
 L("Mean vs median and outliers", [
   "For 2, 3, 3, 4, 100 the mean is 22.4 and the median is 3.",
   "One extreme value pulls the mean and barely moves the median.",
   "That is why typical income or house prices are reported as medians.",
   "With an even count the median is the average of the two middle values: 1, 2, 3, 4 gives 2.5."],
  [("mean 22.4", r"22\.4"), ("median 3", r"(?i)median"), ("outlier", r"(?i)extreme|outlier"), ("income", r"(?i)income|house"), ("2.5", r"2\.5")]),
 L("HTTP caching: max-age, no-cache, no-store, ETag", [
   "Cache-Control: max-age=3600 lets a cache reuse a response for one hour without asking the server.",
   "no-cache means the cache may store the response but must check with the server before each reuse.",
   "no-store means never store the response.",
   "With an ETag the client sends If-None-Match; if nothing changed the server answers 304 Not Modified with no body."],
  [("max-age", r"max-age=3600"), ("no-cache", r"no-cache"), ("no-store", r"no-store"), ("If-None-Match", r"If-None-Match"), ("304", r"304")]),
 L("Python's mutable default argument trap", [
   "Default values are evaluated once, when def runs.",
   "def add(item, items=[]) shares one list: add(1) returns [1], then add(2) returns [1, 2].",
   "Fix: items=None, then inside: if items is None: items = [].",
   "Immutable defaults such as 0 or None are safe."],
  [("evaluated once", r"(?i)once"), ("def add", r"items=\[\]"), ("[1, 2]", r"\[1, 2\]"), ("None fix", r"items is None"), ("immutable", r"(?i)immutable")]),
 L("Photosynthesis: where the oxygen comes from", [
   "Overall: 6CO2 + 6H2O + light energy -> C6H12O6 + 6O2.",
   "Light-dependent reactions in the thylakoid membranes split water, release O2, and make ATP and NADPH.",
   "The Calvin cycle in the stroma uses ATP and NADPH to fix CO2 into sugar.",
   "The released oxygen comes from water, not from carbon dioxide."],
  [("equation", r"C6H12O6"), ("thylakoid", r"(?i)thylakoid"), ("ATP NADPH", r"NADPH"), ("Calvin", r"(?i)calvin"), ("stroma", r"(?i)stroma")]),
 L("Bayes' theorem and false positives", [
   "A disease affects 1% of people; a test detects 90% of sick people and wrongly flags 9% of healthy people.",
   "Out of 1,000 people: 10 sick, 9 test positive; of 990 healthy about 89 test positive.",
   "So P(sick | positive) is about 9 / 98, roughly 9%, not 90%.",
   "P(positive | sick) and P(sick | positive) are different numbers."],
  [("1%", r"1 ?%"), ("1000 people", r"1,?000"), ("89", r"\b89\b"), ("9/98", r"98"), ("conditional", r"P\(")]),
 L("French passé composé with être", [
   "A fixed list of about 17 verbs (aller, venir, partir, arriver, naître, mourir...) and all reflexive verbs use être; not every movement verb is on it: marcher and courir take avoir.",
   "With être the past participle agrees with the subject: elle est allée, ils sont partis.",
   "With avoir there is no agreement with the subject: elle a mangé.",
   "\"J'ai allé\" is wrong; the correct form is je suis allé (allée for a woman)."],
  [("être", r"être"), ("est allée", r"est allée"), ("sont partis", r"sont partis"), ("a mangé", r"a mangé"), ("je suis allé", r"suis allé")]),
 L("The TCP three-way handshake", [
   "The client sends SYN with initial sequence number x.",
   "The server answers SYN-ACK with its own sequence number y and acknowledgment number x + 1.",
   "The client sends ACK with acknowledgment number y + 1; only then does data flow.",
   "UDP has no handshake: it just sends datagrams."],
  [("SYN", r"\bSYN\b"), ("SYN-ACK", r"SYN-ACK"), ("x + 1", r"x ?\+ ?1"), ("y + 1", r"y ?\+ ?1"), ("UDP", r"UDP")]),
]
