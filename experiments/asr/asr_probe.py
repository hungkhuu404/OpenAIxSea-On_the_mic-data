"""Vietnamese ASR probe for live-commerce audio.

Runs one short clip (default 2 minutes) through several OpenAI transcription
configurations and writes a side-by-side report, so the team can pick an ASR
setup before D-Day. This is a de-risking experiment, not product code.

Usage:
    python asr_probe.py VIDEO_OR_AUDIO [--start 0] [--duration 120]
                        [--reference ref.txt] [--keywords kw.txt]
                        [--only diarize_vi,transcribe_vi] [--dry-run]

Needs OPENAI_API_KEY (unless --dry-run) and ffmpeg (on PATH, or the
`imageio-ffmpeg` pip package). Only stdlib + requests otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
import wave
from datetime import datetime
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # documented transcription upload limit
RETRY_STATUSES = {429, 500, 502, 503, 504}


# --------------------------------------------------------------------------- audio

def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg not found. Install it, or: python -m pip install --user imageio-ffmpeg")


def extract_clip(ffmpeg: str, src: Path, dst: Path, start: float, duration: float) -> None:
    """Mono 16 kHz PCM WAV: 2 min is about 3.8 MB, far below the upload limit."""
    cmd = [ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
           "-ss", str(start), "-t", str(duration), "-i", str(src),
           "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(dst)]
    subprocess.run(cmd, check=True)


def wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / float(w.getframerate())


def cut_wav(src: Path, dst: Path, start: float, end: float) -> None:
    """Cut a WAV in-process (no ffmpeg call per segment)."""
    with wave.open(str(src), "rb") as r:
        rate = r.getframerate()
        r.setpos(max(0, int(start * rate)))
        frames = r.readframes(max(0, int((end - start) * rate)))
        params = r.getparams()
    with wave.open(str(dst), "wb") as w:
        w.setparams(params)
        w.writeframes(frames)


# --------------------------------------------------------------------------- API

def expand_fields(fields: dict, keywords: list[str]) -> list[tuple[str, str]]:
    """Form fields as (name, value) pairs; lists become repeated `name[]` entries."""
    out: list[tuple[str, str]] = []
    for name, value in fields.items():
        if value == "$KEYWORDS":
            value = keywords
        if isinstance(value, list):
            key = name if name.endswith("[]") else name + "[]"
            out.extend((key, str(v)) for v in value)
        else:
            out.append((name, str(value)))
    return out


def transcribe(base_url: str, api_key: str, audio: Path, model: str,
               fields: list[tuple[str, str]], timeout: float = 300) -> dict:
    url = base_url.rstrip("/") + "/audio/transcriptions"
    data = [("model", model)] + fields
    last: dict = {}
    for attempt in range(3):
        t0 = time.monotonic()
        try:
            with audio.open("rb") as fh:
                resp = requests.post(url, headers={"Authorization": f"Bearer {api_key}"},
                                     data=data, files={"file": (audio.name, fh, "audio/wav")},
                                     timeout=timeout)
        except requests.RequestException as exc:
            last = {"ok": False, "http_status": None, "error": f"{type(exc).__name__}: {exc}",
                    "latency_s": round(time.monotonic() - t0, 2)}
            time.sleep(2 ** attempt)
            continue
        latency = round(time.monotonic() - t0, 2)
        try:
            body = resp.json()
        except ValueError:
            body = {"raw_text": resp.text}
        last = {"ok": resp.ok, "http_status": resp.status_code, "latency_s": latency,
                "request_id": resp.headers.get("x-request-id"), "body": body}
        if not resp.ok:
            last["error"] = (body.get("error") or {}).get("message") if isinstance(body, dict) else resp.text
        if resp.status_code not in RETRY_STATUSES:
            break
        time.sleep(2 ** attempt)
    return last


def normalize_body(body: dict) -> dict:
    """Map diarized_json / verbose_json / json / text responses onto one shape."""
    if not isinstance(body, dict):
        return {"text": str(body), "segments": None}
    text = body.get("text") or body.get("raw_text") or ""
    segments = None
    if isinstance(body.get("segments"), list):
        segments = [{"speaker": s.get("speaker"),
                     "start": s.get("start"),
                     "end": s.get("end"),
                     "text": (s.get("text") or "").strip()}
                    for s in body["segments"]]
        if not text:
            text = " ".join(s["text"] for s in segments)
    return {"text": text.strip(), "segments": segments}


# --------------------------------------------------------------------------- metrics

PUNCT = re.compile(r"[^\w\s]", re.UNICODE)


def norm_text(s: str, strip_tones: bool = False) -> str:
    s = unicodedata.normalize("NFC", s).lower()
    if strip_tones:
        s = "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))
        s = s.replace("đ", "d")
    s = PUNCT.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def edit_distance(a: list, b: list) -> int:
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, y in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y))
        prev = cur
    return prev[-1]


def error_rates(hyp: str, ref: str) -> dict:
    """Syllable error rate (Vietnamese words are space-separated syllables) and CER."""
    h, r = norm_text(hyp), norm_text(ref)
    if not r:
        return {}
    return {
        "syllable_er": round(edit_distance(h.split(), r.split()) / len(r.split()), 4),
        "cer": round(edit_distance(list(h.replace(" ", "")), list(r.replace(" ", ""))) / len(r.replace(" ", "")), 4),
        "cer_no_tones": round(edit_distance(list(norm_text(hyp, True).replace(" ", "")),
                                            list(norm_text(ref, True).replace(" ", "")))
                              / len(norm_text(ref, True).replace(" ", "")), 4),
    }


def keyword_recall(text: str, keywords: list[str]) -> dict:
    exact = norm_text(text)
    loose = norm_text(text, strip_tones=True)
    hits = [k for k in keywords if norm_text(k) in exact]
    loose_hits = [k for k in keywords if norm_text(k, True) in loose]
    return {"keywords": len(keywords), "exact_hits": len(hits), "toneless_hits": len(loose_hits),
            "missed": [k for k in keywords if k not in loose_hits]}


def segment_stats(segments: list[dict] | None) -> dict:
    if not segments:
        return {"segments": 0, "speakers": 0, "has_timestamps": False}
    speakers = {s.get("speaker") for s in segments if s.get("speaker") is not None}
    timed = all(isinstance(s.get("start"), (int, float)) and isinstance(s.get("end"), (int, float))
                for s in segments)
    lengths = [s["end"] - s["start"] for s in segments if timed]
    return {"segments": len(segments), "speakers": len(speakers), "has_timestamps": timed,
            "mean_segment_s": round(sum(lengths) / len(lengths), 2) if lengths else None}


# --------------------------------------------------------------------------- hybrid

def merge_segments(segments: list[dict], min_s: float, max_s: float) -> list[dict]:
    """Join consecutive same-speaker segments into windows of min_s..max_s seconds."""
    merged: list[dict] = []
    for s in segments:
        if (merged and merged[-1]["speaker"] == s["speaker"]
                and merged[-1]["end"] - merged[-1]["start"] < min_s
                and s["end"] - merged[-1]["start"] <= max_s):
            merged[-1]["end"] = s["end"]
        else:
            merged.append({"speaker": s["speaker"], "start": s["start"], "end": s["end"]})
    return merged


def run_hybrid(variant: dict, results: dict, clip: Path, workdir: Path, base_url: str,
               api_key: str, keywords: list[str]) -> dict:
    """Speaker turns + timestamps from a diarize run, text from a second model per turn."""
    source = next((results[v] for v in variant["segments_from"] if results.get(v, {}).get("ok")
                   and results[v]["normalized"]["segments"]), None)
    if source is None:
        return {"ok": False, "error": "no successful diarize run to take segments from"}
    turns = merge_segments(source["normalized"]["segments"], variant.get("min_turn_s", 4),
                           variant.get("max_turn_s", 30))
    fields = expand_fields(variant["fields"], keywords)
    out_segments, latency, errors = [], 0.0, []
    for i, t in enumerate(turns):
        part = workdir / f"turn_{i:03d}.wav"
        cut_wav(clip, part, t["start"], t["end"])
        r = transcribe(base_url, api_key, part, variant["model"], fields)
        latency += r.get("latency_s") or 0
        text = normalize_body(r.get("body", {}))["text"] if r.get("ok") else ""
        if not r.get("ok"):
            errors.append(f"turn {i}: {r.get('error')}")
        out_segments.append({**t, "text": text})
    return {"ok": not errors or len(errors) < len(turns), "http_status": None,
            "latency_s": round(latency, 2), "calls": len(turns), "errors": errors[:5],
            "normalized": {"text": " ".join(s["text"] for s in out_segments), "segments": out_segments}}


# --------------------------------------------------------------------------- report

def fmt_ts(x) -> str:
    return f"{int(x // 60):02d}:{x % 60:04.1f}" if isinstance(x, (int, float)) else "-"


def write_report(run_dir: Path, meta: dict, results: dict, reference: str | None) -> Path:
    lines = [f"# ASR probe — {meta['started_at']}", "",
             f"- Source: `{meta['source']}` · clip {meta['start']}s + {meta['clip_seconds']:.1f}s",
             f"- Keywords: {len(meta['keywords'])} · Reference transcript: {'yes' if reference else 'no'}",
             f"- Estimated spend: ${meta['estimated_usd']:.4f}", "",
             "| Variant | Model | OK | HTTP | Latency s | Segs | Speakers | Timestamps | Syllable ER | CER | KW hits (exact/toneless) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for vid, r in results.items():
        st = r.get("segment_stats", {})
        er = r.get("error_rates", {})
        kw = r.get("keyword_recall", {})
        lines.append(f"| {vid} | {r.get('model')} | {'✅' if r.get('ok') else '❌'} | {r.get('http_status') or '-'} "
                     f"| {r.get('latency_s', '-')} | {st.get('segments', '-')} | {st.get('speakers', '-')} "
                     f"| {st.get('has_timestamps', '-')} | {er.get('syllable_er', '-')} | {er.get('cer', '-')} "
                     f"| {kw.get('exact_hits', '-')}/{kw.get('toneless_hits', '-')} of {kw.get('keywords', '-')} |")
    lines.append("")
    for vid, r in results.items():
        lines += [f"## {vid}", ""]
        if not r.get("ok"):
            lines += [f"**Error:** {r.get('error') or r.get('errors')}", ""]
            continue
        if r.get("keyword_recall", {}).get("missed"):
            lines.append(f"Missed keywords: {', '.join(r['keyword_recall']['missed'])}")
        segs = r["normalized"].get("segments") or []
        if segs:
            lines += ["", "| Start | End | Speaker | Text |", "|---|---|---|---|"]
            for s in segs[:15]:
                lines.append(f"| {fmt_ts(s.get('start'))} | {fmt_ts(s.get('end'))} | {s.get('speaker')} "
                             f"| {s.get('text', '').replace('|', '/')} |")
        else:
            lines += ["", "> " + r["normalized"]["text"][:1200]]
        lines.append("")
    path = run_dir / "report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# --------------------------------------------------------------------------- main

def load_lines(path: str | None) -> list[str]:
    if not path:
        return []
    return [ln.strip() for ln in Path(path).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", help="video or audio file")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--duration", type=float, default=120.0)
    ap.add_argument("--variants", default=str(HERE / "variants.json"))
    ap.add_argument("--only", help="comma-separated variant ids")
    ap.add_argument("--reference", help="human-corrected transcript of the same clip (UTF-8)")
    ap.add_argument("--keywords", default=str(HERE / "keywords.txt"), help="one keyword per line")
    ap.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    ap.add_argument("--out", default=str(HERE / "runs"))
    ap.add_argument("--dry-run", action="store_true", help="extract audio and print the plan; no API calls")
    args = ap.parse_args()

    src = Path(args.media)
    if not src.is_file():
        sys.exit(f"not found: {src}")
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key and not args.dry_run:
        sys.exit("OPENAI_API_KEY is not set (use --dry-run to test the setup without it)")

    variants = json.loads(Path(args.variants).read_text(encoding="utf-8"))["variants"]
    if args.only:
        wanted = set(args.only.split(","))
        variants = [v for v in variants if v["id"] in wanted]
    keywords = load_lines(args.keywords)
    reference = "\n".join(load_lines(args.reference)) if args.reference else None

    started = datetime.now()
    run_dir = Path(args.out) / started.strftime("%Y%m%d-%H%M%S")
    (run_dir / "raw").mkdir(parents=True, exist_ok=True)
    clip = run_dir / "clip.wav"
    extract_clip(find_ffmpeg(), src, clip, args.start, args.duration)
    seconds = wav_seconds(clip)
    if clip.stat().st_size > MAX_UPLOAD_BYTES:
        sys.exit(f"clip is {clip.stat().st_size / 1e6:.1f} MB, above the 25 MB limit; shorten --duration")

    minutes = seconds / 60
    estimate = sum(v.get("usd_per_min", 0) * minutes for v in variants)
    meta = {"started_at": started.isoformat(timespec="seconds"), "source": src.name, "start": args.start,
            "clip_seconds": seconds, "keywords": keywords, "estimated_usd": estimate,
            "variants": [v["id"] for v in variants], "base_url": args.base_url}
    print(f"clip: {seconds:.1f}s, {clip.stat().st_size / 1e6:.2f} MB -> {run_dir}")
    for v in variants:
        print(f"  {v['id']:<18} {v['model']:<28} {json.dumps(expand_fields(v['fields'], keywords), ensure_ascii=False)[:120]}")
    print(f"estimated spend: ${estimate:.4f}")
    if args.dry_run:
        (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return 0

    results: dict = {}
    for v in variants:
        print(f"-> {v['id']} ...", flush=True)
        if v.get("type") == "hybrid":
            turns_dir = run_dir / f"turns_{v['id']}"
            turns_dir.mkdir(exist_ok=True)
            r = run_hybrid(v, results, clip, turns_dir, args.base_url, api_key, keywords)
        else:
            r = transcribe(args.base_url, api_key, clip, v["model"], expand_fields(v["fields"], keywords))
            (run_dir / "raw" / f"{v['id']}.json").write_text(
                json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
            r["normalized"] = normalize_body(r.get("body", {})) if r.get("ok") else {"text": "", "segments": None}
            r.pop("body", None)
        r["model"] = v["model"]
        if r.get("ok"):
            r["segment_stats"] = segment_stats(r["normalized"]["segments"])
            r["keyword_recall"] = keyword_recall(r["normalized"]["text"], keywords)
            if reference:
                r["error_rates"] = error_rates(r["normalized"]["text"], reference)
        results[v["id"]] = r
        print(f"   ok={r.get('ok')} http={r.get('http_status')} {r.get('error') or ''}")

    (run_dir / "results.json").write_text(json.dumps({"meta": meta, "results": results},
                                                     ensure_ascii=False, indent=2), encoding="utf-8")
    report = write_report(run_dir, meta, results, reference)
    if not reference:
        best = max((r for r in results.values() if r.get("ok")),
                   key=lambda r: r["keyword_recall"]["toneless_hits"], default=None)
        if best:
            (run_dir / "reference.todo.txt").write_text(
                "# Sửa tay transcript này cho đúng từng chữ rồi chạy lại với --reference\n"
                + best["normalized"]["text"] + "\n", encoding="utf-8")
    print(f"report: {report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
