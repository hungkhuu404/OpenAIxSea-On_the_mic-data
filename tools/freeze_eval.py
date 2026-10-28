"""Freeze and verify labelled eval sets with a commit-reveal hash.

Before D-Day: publish FREEZE.json (hashes + counts only) in the public
"existing project" repo, keep the held-out JSONL private. After the on-day
build is frozen, reveal the JSONL; anyone can rerun `verify` and see it
is byte-for-byte the set committed earlier.

    python freeze_eval.py freeze  golden.jsonl heldout.jsonl [-o FREEZE.json] [--draft]
    python freeze_eval.py verify  FREEZE.json golden.jsonl heldout.jsonl
    python freeze_eval.py overlap pool.jsonl heldout.jsonl [--threshold 0.8]

Stdlib only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

TOOL_VERSION = "1"
LABELS = {"green", "yellow", "red"}
REQUIRED = ("case_id", "sku_id", "text", "label", "label_status", "source_url")


def nfc(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, list):
        return [nfc(x) for x in obj]
    if isinstance(obj, dict):
        return {nfc(k): nfc(v) for k, v in obj.items()}
    return obj


def load(path: Path) -> list[dict]:
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if line.strip():
            try:
                rows.append(nfc(json.loads(line)))
            except json.JSONDecodeError as exc:
                sys.exit(f"{path.name}:{n}: invalid JSON ({exc})")
    return rows


def canonical_bytes(rows: list[dict]) -> bytes:
    """Sorted by case_id, sorted keys, compact separators, LF, trailing newline."""
    lines = [json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
             for r in sorted(rows, key=lambda r: r["case_id"])]
    return ("\n".join(lines) + "\n").encode("utf-8")


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFC", s).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def bigrams(s: str) -> set:
    toks = norm_text(s).split()
    return {tuple(toks[i:i + 2]) for i in range(len(toks) - 1)} or {tuple(toks)}


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def validate(name: str, rows: list[dict], draft: bool) -> list[str]:
    errs = []
    for r in rows:
        missing = [k for k in REQUIRED if not r.get(k)]
        if missing:
            errs.append(f"{name}:{r.get('case_id', '?')}: missing {missing}")
        if r.get("label") not in LABELS:
            errs.append(f"{name}:{r.get('case_id')}: label must be one of {sorted(LABELS)}")
        if not draft and r.get("label_status") != "human_confirmed":
            errs.append(f"{name}:{r.get('case_id')}: label_status is '{r.get('label_status')}', "
                        "need 'human_confirmed' (or pass --draft)")
    return errs


def near_duplicates(a: list[dict], b: list[dict], threshold: float) -> list[tuple]:
    grams_b = [(r["case_id"], bigrams(r["text"]), norm_text(r["text"])) for r in b]
    hits = []
    for r in a:
        ga, ta = bigrams(r["text"]), norm_text(r["text"])
        for cid, gb, tb in grams_b:
            score = 1.0 if ta == tb else jaccard(ga, gb)
            if score >= threshold:
                hits.append((r["case_id"], cid, round(score, 3)))
    return hits


def summarize(rows: list[dict]) -> dict:
    dates = sorted(r["source_date"] for r in rows if r.get("source_date"))
    return {"n": len(rows),
            "labels": dict(Counter(r["label"] for r in rows)),
            "skus": dict(Counter(r["sku_id"] for r in rows)),
            "source_types": dict(Counter(r.get("source_type", "?") for r in rows)),
            "source_date_range": [dates[0], dates[-1]] if dates else None}


def cmd_freeze(args) -> int:
    sets = {Path(p).name: load(Path(p)) for p in args.files}
    errs = [e for name, rows in sets.items() for e in validate(name, rows, args.draft)]
    ids = Counter(r["case_id"] for rows in sets.values() for r in rows)
    errs += [f"duplicate case_id across sets: {cid}" for cid, c in ids.items() if c > 1]
    names = list(sets)
    for i, j in product(range(len(names)), repeat=2):
        if i < j:
            for x, y, s in near_duplicates(sets[names[i]], sets[names[j]], args.threshold):
                errs.append(f"near-duplicate across {names[i]} / {names[j]}: {x} ~ {y} ({s})")
    if errs:
        print("\n".join(errs))
        return 1
    files = {name: {"sha256": hashlib.sha256(canonical_bytes(rows)).hexdigest(), **summarize(rows)}
             for name, rows in sets.items()}
    root = hashlib.sha256("".join(f"{n}:{files[n]['sha256']}\n" for n in sorted(files)).encode()).hexdigest()
    manifest = {"tool": f"freeze_eval.py v{TOOL_VERSION}", "draft": args.draft,
                "frozen_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "canonicalization": "NFC; rows sorted by case_id; json sort_keys, separators (',',':'), "
                                    "ensure_ascii=False; LF; trailing newline; SHA-256",
                "files": files, "root_sha256": root}
    Path(args.out).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}{'  (DRAFT: labels not human-confirmed)' if args.draft else ''}")
    for n, f in files.items():
        print(f"  {n}: n={f['n']} sha256={f['sha256']}")
    summary = ", ".join(f"{n} n={f['n']}" for n, f in files.items())
    print(f"commit message: freeze(eval): {summary} root={root[:16]}")
    return 0


def cmd_verify(args) -> int:
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    ok = True
    for p in args.files:
        name = Path(p).name
        want = manifest["files"].get(name, {}).get("sha256")
        got = hashlib.sha256(canonical_bytes(load(Path(p)))).hexdigest()
        status = "OK" if want == got else ("NOT IN MANIFEST" if want is None else "MISMATCH")
        ok &= status == "OK"
        print(f"{status:<16} {name} {got}")
    return 0 if ok else 1


def cmd_overlap(args) -> int:
    a, b = load(Path(args.pool)), load(Path(args.heldout))
    hits = near_duplicates(a, b, args.threshold)
    for x, y, s in hits:
        print(f"{x} ~ {y} ({s})")
    print(f"{len(hits)} near-duplicate pair(s) at threshold {args.threshold}")
    return 1 if hits else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("freeze")
    f.add_argument("files", nargs="+")
    f.add_argument("-o", "--out", default="FREEZE.json")
    f.add_argument("--draft", action="store_true", help="allow labels that are not human_confirmed")
    f.add_argument("--threshold", type=float, default=0.8, help="bigram Jaccard for near-duplicates")
    v = sub.add_parser("verify")
    v.add_argument("manifest")
    v.add_argument("files", nargs="+")
    o = sub.add_parser("overlap")
    o.add_argument("pool")
    o.add_argument("heldout")
    o.add_argument("--threshold", type=float, default=0.8)
    args = ap.parse_args()
    return {"freeze": cmd_freeze, "verify": cmd_verify, "overlap": cmd_overlap}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
