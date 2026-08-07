# sagan-start

Starts a run of the Sagan agent loop in a project that already has a `.sagan/`
folder. Type `/sagan-start`.

## What it is

`sagan-wire` installs Sagan into a project. Nothing ran it. This does: it pulls
your tickets out of Linear into local markdown files, checks each one actually
says what "done" means, asks you whether you're doing one ticket or a sprint,
writes the run into the audit trail, and hands you a brief.

It deliberately **stops before putting agents to work.** You read the brief and
decide. That boundary is the point of v1 — the run opens under your eye.

## What you get

- A markdown file per ticket in `tickets/` that every agent can read directly,
  so nobody has to retype the ticket into a prompt (and quietly change it).
- A hard stop on any ticket with no acceptance criteria. Not a warning — a
  non-zero exit code.
- One batch of questions instead of a dozen interruptions.
- A `run.started` line in `.sagan/ledger/events.jsonl` and a run brief saved
  next to it.

## How to run

| You want | Type |
|---|---|
| The normal thing | `/sagan-start` |
| Skip the scope question | `/sagan-start --scope=sprint` |
| One known ticket | `/sagan-start --ticket=WHA-133` |
| See the plan, change nothing | `/sagan-start --dry-run` |
| Tracker is down / you're offline | `/sagan-start --no-fetch` |
| Push a ticket's notes back to Linear | `/sagan-start --writeback=WHA-133` |

## What it needs

- A project with a `.sagan/` folder (run `/sagan-wire` first if not).
- `python3` — any 3.x. No pip installs, no API keys, no config.
- For Linear tickets: the Linear connector enabled in your Claude session.
  The scripts never talk to Linear themselves; the session does, and pipes
  the result in.
- Git, if you want evidence bound to a commit — it works without, and says so.

## How it works

The split is the whole design: **Linear owns the ticket's intent, the repo owns
its execution.**

Linear owns the title, status, priority, assignee and description. Those get
overwritten in the local file on every fetch. The repo owns the acceptance
criteria and the blocks where agents write build notes, QA results and
decisions. A fetch never touches those — not "tries not to", *cannot*: the
script copies that region across byte-for-byte, and if it can't find the region
in a file it refuses to write rather than risk clobbering an agent's work.

Going the other way, notes go back to Linear **word for word**. The script
builds the comment text out of the file and hands it over finished, so there's
no step where a model gets to rewrite it into a summary.

Five small scripts do the mechanical parts (`preflight`, `mirror`, `precheck`,
`ledger`, `writeback`) so those parts are code rather than something a model has
to remember. The judgment parts — which tickets, which questions, what the
answers mean — stay with the session.

## What it doesn't do

- Dispatch builders, critics or verifiers. That's yours, after the brief.
- Run tickets in parallel. Sprint mode batches the *planning*; builds still go
  one at a time, because nothing at v0 would catch two agents editing the same
  file.
- Write acceptance criteria for you. It only refuses to proceed without them.
