# cert-study

Private study workspace for Lloyd Johnson's certification path. Not part of the public portfolio.

Everything here is study material. Practice questions are AI-generated unless marked otherwise and are **unverified until checked against the official exam objectives**. Do not copy anything from this repository into the public portfolio without reviewing it first.

## Layout

```text
roadmap.md                 Order of certs, target windows, costs, and how each is paid for
CLAUDE.md                  How Claude runs study sessions in this repo (cloud or local)
certs/<cert>/README.md     Exam facts, domains and weights, resources, status
certs/<cert>/questions.json  Question bank for that cert
certs/<cert>/labs.md       Hands-on labs, mostly in the Hyper-V lab (DC01, WS01, ...)
certs/<cert>/notes.md      Your own notes
certs/<cert>/objectives.md Objective outline built from the official PDF
certs/<cert>/topics.json   Every topic in that outline, with an ID that questions are tagged with
reference/                 Official PDFs and course notes; ignored by Git, so it stays on the machine where you put it
progress/attempts.csv      Every answered question (written by the quiz tool and by Claude)
tools/quiz.py              Terminal quiz runner (Python 3, no extra packages)
```

## Quick start

Run these from the repository root. On Windows use `python`; on Linux or macOS use `python3`.

```text
python tools/quiz.py list                                 # certs and question counts
python tools/quiz.py quiz comptia-network-plus -n 10      # 10 questions
python tools/quiz.py quiz comptia-security-plus --weak    # missed questions first, then unseen
python tools/quiz.py quiz comptia-network-plus --domain 1.0
python tools/quiz.py report comptia-network-plus          # accuracy by domain and objective
python tools/quiz.py coverage comptia-network-plus        # which official topics have questions
python tools/quiz.py validate                             # check every question bank
```

Answer with the letter (`b`), or letters for "choose two" questions (`ac`). Type `q` to stop.

After a session, commit `progress/attempts.csv` so your history follows you between your PC and cloud sessions:

```text
git add progress/attempts.csv
git commit -m "Log study session"
git push
```

## Using it with Claude Code

- **Local session on your PC:** best for labs, because Claude can run real Windows and Hyper-V commands (`ipconfig`, `tracert`, `Get-VM`, PowerShell Direct into lab VMs).
- **Cloud session:** best for building question banks and PBQ simulators, and for quizzing from any device.

Both read `CLAUDE.md`. Ask for things like "quiz me on Security+ domain 4, weakest first" or "walk me through lab N-03".

## Reference files

Put official objectives PDFs and course notes in `reference/` (for example `reference/comptia-network-plus-n10-009-exam-objectives.pdf`). Git ignores the folder, so CompTIA's and Professor Messer's documents are never pushed to GitHub. Claude uses them to check questions and to build `objectives.md`. On your PC, copy them in once. In a cloud session, upload them again when they are needed.
