#!/usr/bin/env python3
"""Build the verbatim Linear comment payload for a mirrored ticket.

I/O: stdout JSON {ticket, url, body, sha, changed, blocks} · stderr one line
     · exit 3 when the ticket is not mirrored, 0 otherwise.

Why a script: the write-back rule is that repo-owned blocks go back to Linear
**word for word**, not summarized. This script copies the block bodies out of
the file byte-for-byte and hands the session a finished `body` string to post
via the Linear MCP. The session posts what it is given; it never composes the
text, so there is no paraphrase step to forget.

Only the header line is generated (ticket id, git SHA, role ids) — everything
below it is a byte copy of the file.

Re-run with --record after a successful post to stamp the content hash, so an
unchanged ticket does not spam the issue with duplicate comments.
"""
import argparse
import datetime
import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _sagan as S  # noqa: E402

DEFAULT_BLOCKS = ("frontend", "qa", "decisions")


def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--ticket", required=True)
    ap.add_argument("--blocks", default=",".join(DEFAULT_BLOCKS),
                    help="repo-owned blocks to send back (default: %s)"
                         % ",".join(DEFAULT_BLOCKS))
    ap.add_argument("--record", action="store_true",
                    help="stamp last_writeback in the mirror after a successful post")
    ap.add_argument("--agent", action="store_true")
    a = ap.parse_args()

    root = S.project_root(a.project)
    cfg = S.read_sagan_yaml(S.sagan_yaml(root))
    path = os.path.join(S.tickets_dir(root, cfg), "%s.md" % a.ticket.strip())
    if not os.path.isfile(path):
        print("not mirrored: %s" % a.ticket, file=sys.stderr)
        return S.emit({"error": "not-mirrored", "ticket": a.ticket}, 3)

    with io.open(path, encoding="utf-8") as fh:
        text = fh.read()
    fm, _order, body = S.split_frontmatter(text)
    region = S.extract_region(body, S.REPO_START, S.REPO_END)
    if region is None:
        print("no repo-owned region — re-run the mirror", file=sys.stderr)
        return S.emit({"error": "no-region", "ticket": a.ticket}, 3)

    blocks = S.blocks_from_region(region)
    wanted = [b.strip().lower() for b in a.blocks.split(",") if b.strip()]

    parts, included = [], []
    for key in wanted:
        content = (blocks.get(key) or "").strip("\n")
        if not [ln for ln in content.splitlines()
                if ln.strip() and not ln.strip().startswith("<!--")]:
            continue
        title = S.BLOCK_TITLES.get(key, key.title())
        parts.append("## %s\n\n%s" % (title, content))  # byte copy of the block
        included.append(key)

    payload_body = "\n\n".join(parts)
    digest = content_hash(payload_body)
    changed = fm.get("last_writeback", "") != digest

    sha = S.head_sha(root) or ""
    meta = ["**Sagan sync**"]
    if sha:
        meta.append("`%s`" % sha[:7])
    for field, label in (("builder_id", "builder"), ("verifier_id", "verifier"),
                         ("evidence_sha", "evidence")):
        if fm.get(field):
            meta.append("%s `%s`" % (label, fm[field]))
    header = " · ".join(meta)
    full = header + "\n\n" + payload_body if payload_body else ""

    if a.record and payload_body:
        new_fm, order = dict(fm), list(_order)
        new_fm["last_writeback"] = digest
        new_fm["last_writeback_at"] = datetime.date.today().isoformat()
        for k in ("last_writeback", "last_writeback_at"):
            if k not in order:
                order.append(k)
        S.atomic_write(path, S.render_frontmatter([(k, new_fm[k]) for k in order])
                       + body)
        print("recorded last_writeback=%s" % digest, file=sys.stderr)

    print("%s — %d block(s), %s" % (a.ticket, len(included),
                                    "changed" if changed else "unchanged"),
          file=sys.stderr)
    return S.emit({
        "ticket": a.ticket,
        "url": fm.get("url", ""),
        "blocks": included,
        "changed": changed,
        "hash": digest,
        "sha": sha,
        "body": full,
        "post": bool(full) and changed,
    }, 0)


if __name__ == "__main__":
    sys.exit(main())
