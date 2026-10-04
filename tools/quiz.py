#!/usr/bin/env python3
"""Terminal quiz runner for the cert-study question banks.

Usage:
  quiz.py list
  quiz.py quiz <cert> [-n N] [--domain D] [--weak]
  quiz.py report <cert>
  quiz.py validate

Question banks live in certs/<cert>/questions.json. Every answer is appended
to progress/attempts.csv so history carries across sessions and machines.
Uses only the Python standard library.
"""

import argparse
import csv
import datetime
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CERTS = ROOT / "certs"
ATTEMPTS = ROOT / "progress" / "attempts.csv"
FIELDS = ["timestamp", "cert", "question_id", "domain", "objective", "correct", "source"]
REQUIRED = ["id", "domain", "objective", "question", "choices", "answer", "explanation", "source", "verified"]


def load_bank(cert):
    path = CERTS / cert / "questions.json"
    if not path.exists():
        sys.exit(f"No question bank at {path}. Run 'list' to see certs.")
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def answers_of(q):
    a = q["answer"]
    return sorted(a) if isinstance(a, list) else [a]


def load_attempts(cert=None):
    if not ATTEMPTS.exists():
        return []
    with ATTEMPTS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if cert is None or r["cert"] == cert]


def record(cert, q, correct):
    ATTEMPTS.parent.mkdir(exist_ok=True)
    new = not ATTEMPTS.exists()
    with ATTEMPTS.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({
            "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
            "cert": cert,
            "question_id": q["id"],
            "domain": q["domain"],
            "objective": q["objective"],
            "correct": "1" if correct else "0",
            "source": "quiz",
        })


def weak_order(cert, questions):
    """Most-missed questions first, then never-seen ones, then the rest; ties are shuffled."""
    stats = defaultdict(lambda: [0, 0])  # id -> [misses, hits]
    for r in load_attempts(cert):
        stats[r["question_id"]][0 if r["correct"] == "0" else 1] += 1

    def priority(q):
        misses, hits = stats[q["id"]]
        unseen = 1 if misses + hits == 0 else 0
        return (3 * (misses - hits) + 2 * unseen, random.random())

    return sorted(questions, key=priority, reverse=True)


def ask(q, number, total):
    """Show one question with shuffled choices. Returns True, False, or None to quit."""
    keys = list(q["choices"])
    shuffled = random.sample(keys, len(keys))
    letters = "ABCDEFGH"[: len(shuffled)]
    mapping = dict(zip(letters, shuffled))
    correct = {letter for letter, key in mapping.items() if key in answers_of(q)}

    print(f"\n[{number}/{total}] {q['id']}  (domain {q['domain']}, objective {q['objective']})")
    print(q["question"])
    for letter in letters:
        print(f"  {letter}. {q['choices'][mapping[letter]]}")
    hint = f" (choose {len(correct)})" if len(correct) > 1 else ""
    while True:
        try:
            raw = input(f"Answer{hint}: ")
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        raw = raw.strip().upper().replace(",", "").replace(" ", "")
        if raw == "Q":
            return None
        if raw and set(raw) <= set(letters) and len(raw) == len(correct):
            break
        print(f"Enter {len(correct)} letter(s) from {letters}, or q to quit.")

    ok = set(raw) == correct
    print("Correct." if ok else f"Incorrect. Answer: {''.join(sorted(correct))}")
    print(q["explanation"])
    if not q.get("verified"):
        print("(AI-generated question, not yet verified against the official objectives.)")
    return ok


def cmd_list(_):
    for d in sorted(p for p in CERTS.iterdir() if p.is_dir()):
        bank = d / "questions.json"
        count = len(json.loads(bank.read_text(encoding="utf-8"))) if bank.exists() else 0
        print(f"{d.name:32} {count:4} questions")


def cmd_quiz(args):
    questions = load_bank(args.cert)
    if args.domain:
        questions = [q for q in questions if q["domain"] == args.domain]
    if not questions:
        sys.exit("No questions match.")
    questions = weak_order(args.cert, questions) if args.weak else random.sample(questions, len(questions))
    questions = questions[: args.n]
    right = asked = 0
    for i, q in enumerate(questions, 1):
        result = ask(q, i, len(questions))
        if result is None:
            break
        record(args.cert, q, result)
        asked += 1
        right += result
    if asked:
        print(f"\nScore: {right}/{asked} ({100 * right // asked}%)")


def cmd_report(args):
    by_domain = defaultdict(lambda: [0, 0])  # domain -> [right, total]
    for r in load_attempts(args.cert):
        by_domain[r["domain"]][0] += r["correct"] == "1"
        by_domain[r["domain"]][1] += 1
    if not by_domain:
        print("No attempts yet.")
        return
    print(f"{'Domain':8} {'Right':>6} {'Total':>6} {'Accuracy':>9}")
    for domain in sorted(by_domain):
        right, total = by_domain[domain]
        print(f"{domain:8} {right:6} {total:6} {100 * right // total:8}%")


def cmd_validate(_):
    problems = 0
    for bank in sorted(CERTS.glob("*/questions.json")):
        try:
            questions = json.loads(bank.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"{bank}: invalid JSON: {e}")
            problems += 1
            continue
        seen = set()
        for q in questions:
            where = f"{bank.parent.name}:{q.get('id', '?')}"
            missing = [k for k in REQUIRED if k not in q]
            if missing:
                print(f"{where}: missing {missing}")
                problems += 1
                continue
            if q["id"] in seen:
                print(f"{where}: duplicate id")
                problems += 1
            seen.add(q["id"])
            if not set(answers_of(q)) <= set(q["choices"]):
                print(f"{where}: answer not among choices")
                problems += 1
            if len(q["choices"]) < 2:
                print(f"{where}: fewer than two choices")
                problems += 1
    print("All question banks valid." if not problems else f"{problems} problem(s) found.")
    sys.exit(1 if problems else 0)


def main():
    p = argparse.ArgumentParser(description="Quiz runner for cert-study question banks.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    q = sub.add_parser("quiz")
    q.add_argument("cert")
    q.add_argument("-n", type=int, default=10, help="number of questions (default 10)")
    q.add_argument("--domain", help="only this domain, for example 1.0")
    q.add_argument("--weak", action="store_true", help="most-missed questions first, then unseen")
    r = sub.add_parser("report")
    r.add_argument("cert")
    sub.add_parser("validate")
    args = p.parse_args()
    {"list": cmd_list, "quiz": cmd_quiz, "report": cmd_report, "validate": cmd_validate}[args.cmd](args)


if __name__ == "__main__":
    main()
