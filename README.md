# VN Live-Commerce Compliance — preparation data & experiments

Preparation material for our entry to the **Sea x OpenAI Regional Codex Hackathon – Vietnam (31 Oct 2026)**

The organisers confirmed (21 Oct 2026) that teams may prepare before the event, and that **only work built during the hackathon is judged**. Everything here was prepared before the event. It is listed in our Declarations PDF and linked from the hackathon repository.

> **No product code lives here.**
> - **Built on the day, in the new hackathon repo:** all product code.
> - **Here:** public data, a held-out set committed by hash, and three small utilities.

> **Status (22 Oct 2026):** the team is still reviewing the case labels. `data/cases/golden.jsonl` and `data/cases/FREEZE.json` will be added when the review is done, **before 31 Oct**. Everything else below is already here.

## Contents

| Path | What | Source / licence |
|---|---|---|
| `data/law/` | **26 articles from 9 Vietnamese legal documents** on live-commerce advertising of health supplements: Law 122/2025 on e-commerce, Decree 248/2026, Decree 15/2018, Decree 115/2018 (as amended by Decree 124/2021), Decree 342/2025, Pharmacy Law, Advertising Law (as amended by Law 75/2025), Decree 87/2026, Criminal Code Art. 198. Verbatim, one file per article. **391 anchor IDs** at clause/point level in `index.json` | Official Gazette (Công báo), cross-checked against a second source. Legal normative documents are not copyright-protected (Law on IP, Art. 15) |
| `data/demo/kera/` | The Kera vegetable-candy case (2024–2025): the product's dossier by date, 58 quotes from press and court reporting (people are referred to by role), a timeline of the 6 livestream sessions, a **re-enactment** transcript assembled from those quotes, and a list of news videos that carry original livestream audio | Press and court reporting, one URL per quote (`SOURCES.md`). The re-enactment is labelled as such; it is not an original recording |
| `data/registry/` | Registry of 72,766 health-supplement product declarations (số ĐKSP, 2018 – 05/2025). 312 recall rows from 77 recall decisions (04/2025 – 06/2026). Notes on why ĐKSP numbers are not unique keys (`DKSP_NOTES.md`). Survey of the public lookup portals (`PORTALS.md`) | Cục An toàn thực phẩm (vfa.gov.vn), public files |
| `data/evidence/` | Evidence packs for 10 products: registration status, ad-content confirmation (GXNQC), declared/permitted claims with a source per line, and regulator warnings | Public product pages, press, VFA warnings. **Not** the official dossier, which is not public. In production, Art. 22(5) of Law 122/2025 requires sellers to provide it to the platform |
| `data/cases/golden.jsonl` | Labelled claim sentences from real public sources (regulator warnings, product pages, video captions, press and court reporting), used as regression tests | Each case has a URL and date. Labels were proposed with an AI assistant and **confirmed by a team member** |
| `data/cases/FREEZE.json` | **SHA-256 commitment of the held-out set.** The set itself stays private until judging, then is revealed for verification | See "Held-out commit-reveal" below |
| `experiments/asr/` | Probe comparing OpenAI transcription models on Vietnamese live-commerce audio, and the decision rule we used | Our code (MIT). No audio is committed |
| `tools/freeze_eval.py`, `tools/apply_review.py`, `tools/yt_fetch.py` | Freeze / verify / overlap-check for labelled eval sets; export the human label review to JSONL; fetch public YouTube captions (no video download) | Our code (MIT) |

**Not published here** (see `.gitignore`):
- raw downloads (`_raw/`), kept locally for provenance;
- `heldout.jsonl` and the candidate/review/stats files, which contain or describe held-out cases;
- ASR runs (audio).

## Held-out commit-reveal

1. **Before the event,** we froze a held-out set of labelled claims. We committed only its hash (`data/cases/FREEZE.json`), never its content.
2. **On the day,** the held-out set is not in the build workspace.
3. **After the on-day build is frozen,** we publish the held-out file. Anyone can check it is the same set:

```bash
python tools/freeze_eval.py verify data/cases/FREEZE.json data/cases/heldout.jsonl
```

This shows the evaluation set was fixed **before** any rule existed. It rules out tuning the set to the rules after the fact.

## Data caveats

- **Declared product claims (công dụng) are not publicly searchable** on the Ministry of Health portals. Demo evidence packs quote labels and public pages, with the URL and date for every line.
- Proposed labels are a starting point. **Only `human_confirmed` labels enter golden or held-out**; `freeze_eval.py` enforces this.
- Company and product names come from public regulator warnings. Names of private individuals are removed.

## Related work

**Shopee Live Producer** (Sea x OpenAI Codex Hackathon Singapore, 06/2026) is a host-side real-time chat assistant that blocks claims contradicting product facts. Our project addresses a different question on the platform side: whether each spoken claim is **permitted by the legal dossier of that exact SKU**, recorded as timestamped evidence that platforms must retain for at least one year (Law 122/2025, Art. 22(7)).
