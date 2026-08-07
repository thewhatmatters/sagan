#!/usr/bin/env python3
"""Shared helpers for sagan-start scripts (paths, targeted sagan.yaml reads,
mirror-file parsing, atomic writes).

Not a script: imported by preflight.py / mirror.py / precheck.py / ledger.py.
Stdlib only — no PyYAML, no network, no secrets.
"""
import io
import json
import os
import re
import shutil
import subprocess
import tempfile

MIRROR_VERSION = 1

# Frontmatter keys the REPO owns. A fetch never overwrites these; they are
# carried across from the existing mirror file. Everything else in the
# frontmatter is Linear-owned and is regenerated on every fetch.
REPO_OWNED_FM = ("builder_id", "verifier_id", "evidence_sha", "blocked_by",
                 "sagan_status", "ac_seeded_from", "migrated_at",
                 "last_writeback", "last_writeback_at")

# Repo-owned keys always emitted, even when empty — sagan.yaml's
# ticket.required_fields expects them to exist on the ticket from day one.
REPO_FM_ALWAYS = ("builder_id", "verifier_id", "evidence_sha")

LINEAR_START = "<!-- sagan:linear-owned:start — regenerated on every fetch; edit in Linear -->"
LINEAR_END = "<!-- sagan:linear-owned:end -->"
REPO_START = "<!-- sagan:repo-owned:start — agents write below; a fetch never touches this region -->"
REPO_END = "<!-- sagan:repo-owned:end -->"

DEFAULT_BLOCKS = ("ac", "frontend", "qa", "decisions")
BLOCK_TITLES = {"ac": "AC", "frontend": "Frontend", "qa": "QA",
                "decisions": "Decisions"}


# ---------------------------------------------------------------- paths ----

def project_root(arg=None):
    return os.path.abspath(arg or os.getcwd())


def sagan_dir(root):
    return os.path.join(root, ".sagan")


def sagan_yaml(root):
    return os.path.join(sagan_dir(root), "sagan.yaml")


def ledger_path(root):
    return os.path.join(sagan_dir(root), "ledger", "events.jsonl")


def tickets_dir(root, cfg=None):
    rel = (cfg or {}).get("ticket.mirror.path") or "tickets"
    return os.path.join(root, rel)


# --------------------------------------------------- targeted yaml read ----

_SCALAR = re.compile(r"^(\s*)([A-Za-z0-9_.-]+):\s*(.*?)\s*$")


def read_sagan_yaml(path):
    """Targeted scalar reader for sagan.yaml — NOT a YAML parser.

    Returns a flat dict of dotted paths -> string values for plain
    `key: value` scalars nested under `key:` headers. Flow maps/lists
    (`{ a: b }`, `[a, b]`) are kept verbatim as their raw string; list
    items (`- x`) are ignored. Sufficient for the handful of settings
    this skill reads; anything richer should be read by the session.
    """
    out = {}
    if not os.path.isfile(path):
        return out
    stack = []  # (indent, key)
    with io.open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            m = _SCALAR.match(line.split(" #")[0])
            if not m:
                continue
            indent, key, val = len(m.group(1)), m.group(2), m.group(3)
            while stack and stack[-1][0] >= indent:
                stack.pop()
            path_key = ".".join([k for _i, k in stack] + [key])
            if val == "":
                stack.append((indent, key))
            else:
                out[path_key] = val
    return out


def truthy(val, default=False):
    if val is None:
        return default
    return str(val).strip().lower() in ("1", "true", "yes", "on", "required")


# ----------------------------------------------------------------- git -----

def git(root, *args):
    """Run a git command; return (ok, stdout). Never raises, never hangs."""
    if not shutil.which("git"):
        return False, ""
    try:
        p = subprocess.run(("git", "-C", root) + args, capture_output=True,
                           text=True, timeout=15)
        return p.returncode == 0, p.stdout.strip()
    except Exception:
        return False, ""


def head_sha(root):
    ok, out = git(root, "rev-parse", "HEAD")
    return out if ok else None


# ------------------------------------------------------- mirror parsing ----

def split_frontmatter(text):
    """Return (frontmatter_dict, ordered_keys, body). No frontmatter -> ({}, [], text)."""
    if not text.startswith("---\n"):
        return {}, [], text
    end = text.find("\n---\n", 3)
    if end == -1:
        return {}, [], text
    fm_raw, body = text[4:end + 1], text[end + 5:]
    fm, order = {}, []
    for line in fm_raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _SCALAR.match(line)
        if m and m.group(1) == "":
            fm[m.group(2)] = m.group(3)
            order.append(m.group(2))
    return fm, order, body


def render_frontmatter(pairs):
    lines = ["---"]
    for k, v in pairs:
        lines.append("%s:%s" % (k, (" " + str(v)) if str(v) != "" else ""))
    lines.append("---")
    return "\n".join(lines) + "\n"


def extract_region(text, start_marker, end_marker):
    """Return the text between markers (exclusive), or None if not delimited."""
    i = text.find(start_marker)
    if i == -1:
        return None
    j = text.find(end_marker, i)
    if j == -1:
        return None
    return text[i + len(start_marker):j]


def blocks_from_region(region):
    """Split a repo-owned region into {heading_lower: body} by `## ` headings."""
    out, cur, buf = {}, None, []
    for line in (region or "").splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf).strip("\n")
            cur, buf = m.group(1).strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip("\n")
    return out


def seed_repo_region(blocks=DEFAULT_BLOCKS, seeded=None):
    """Build an empty repo-owned region with one `## ` heading per block."""
    seeded = seeded or {}
    parts = []
    for b in blocks:
        title = BLOCK_TITLES.get(b, b.replace("_", " ").title())
        body = seeded.get(b, "")
        parts.append("## %s\n\n%s" % (title, body + "\n") if body else "## %s\n" % title)
    return "\n" + "\n\n".join(parts).rstrip("\n") + "\n"


# ---------------------------------------------------------------- write ----

def atomic_write(path, text):
    d = os.path.dirname(os.path.abspath(path))
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".sagan-tmp-")
    try:
        with io.open(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def emit(payload, exit_code=0):
    """Payload -> stdout as JSON (spec A4). Callers put diagnostics on stderr."""
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return exit_code
