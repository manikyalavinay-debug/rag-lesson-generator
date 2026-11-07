# Finish and submit

The brief asks for a GitHub repo, a Google Doc/Notion lesson link and a 15-20 minute face-visible walkthrough video. The implementation, twelve tests and a real successful model run are complete. Use `final/lesson.md` as the final lesson and `final/report.json` as its evaluation evidence. These account-bound steps remain:

1. To reproduce the completed live run, use `python -u app.py --model gemma3:4b --judge-model qwen3:8b --timeout 1800`. A rerun may receive different verdicts; preserve honest evidence.
2. Inspect `final/report.json` and `final/RUN-NOTES.md`. The final lesson passed on candidate 1 after earlier development failures; do not claim the successful run itself needed regeneration.
3. Copy `final/lesson.md` into Google Docs or Notion. Give it the title **Introduction to RAG**. Check layout and reviewer access. The root `lesson.md` remains a curated offline fixture.
4. Create a GitHub repository and upload this project. The successful run is already copied under `examples/live/`. `outputs/` and SQLite memory are ignored by default.
5. Record the face-visible 15-20 minute video using `VIDEO-SCRIPT.md`. Be explicit about the difference between live calls and fixture tests.
6. Add the three real links below and submit them through the assessment form yourself.

| Deliverable | Your link |
|---|---|
| GitHub repo | Not published |
| Final lesson document | Not published |
| Loom walkthrough | Not recorded |

Assessment form from the supplied brief: https://forms.gle/GKMb6wa7HiGFrXvC6 . This package has not submitted the form.

Disclose AI assistance if the hiring process requires it. Review the implementation so you can explain the architecture and trade-offs in your own words.

The separate live deliberate-error accuracy probe is already complete at `examples/live-error-probe/report.json`: Qwen rejected the injected guarantee and quoted it exactly. You can show this recorded evidence and reproduce the probe using `error_probe.py`. Do not describe it as a full-rubric regeneration run.
