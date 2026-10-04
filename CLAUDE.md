# Instructions for Claude: cert-study

This is Lloyd's private certification study repository. Lloyd is a veteran studying for CompTIA Network+ (N10-009) and Security+ (SY0-701), with GRC certifications to follow. See `roadmap.md`.

## Quizzing

- Ask **one question at a time**. When the AskUserQuestion tool is available, use it so the choices are clickable; otherwise list the choices as A to D.
- After each answer, say whether it was right, explain why the correct answer is correct, and explain why each wrong choice is wrong.
- Tag every question with its cert, domain, and objective number (for example `N10-009 2.2`).
- Log every answered question to `progress/attempts.csv` in the same format `tools/quiz.py` uses, with `source` set to `claude`.
- To decide what to ask, run `python3 tools/quiz.py report <cert>` and favor the weakest domains. Weight questions roughly by the exam's domain weights.
- Mix in scenario questions and "choose two" questions, like the real exams. Performance-based questions (PBQs) can be built as HTML simulators.

## Accuracy

- Questions you write are AI-generated. Add them to a bank with `"verified": false` and `"source": "ai-generated"`.
- Never claim a question is from or matches the real exam. Never reproduce copyrighted practice-test content.
- If you are not sure of a fact, say so, and point Lloyd to the official exam objectives or vendor documentation.
- Keep exam facts in each `certs/<cert>/README.md` marked "verify" until Lloyd has checked them against the official source.

## Teaching

- Explain new concepts directly, then check understanding with a question.
- Tie concepts to Lloyd's real systems where it helps: his Hyper-V lab (DC01 at 10.10.20.10, domain `lab.local`), his portfolio SOPs, and his Cloudflare DNS setup for johnsontechnicalsystems.com.

## Labs

- Labs run in the Hyper-V lab on Lloyd's Windows 11 host. Walk through **one step at a time and wait for confirmation**.
- Before any script or risky change, have Lloyd shut the VM down and take a checkpoint.
- Treat lab VMs as disposable. No personal accounts, real passwords, or business email inside them.
- Read-only diagnostics on the host are fine. Ask before anything that changes host networking, firewall rules, or Docker.

## Commits

- Commit messages: a short summary line, a blank line, then one line on why.
- Do not commit anything from inside a lab VM that contains real credentials, real public IP addresses, or serial numbers.
- Do not rewrite or amend commits that are already pushed.
