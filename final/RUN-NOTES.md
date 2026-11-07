# Completed local live run

- Run ID: `20261107T160707Z-126628d1`.
- Date: 7 November 2026.
- Generator: `gemma3:4b` through local Ollama.
- Evaluator: `qwen3:8b` through local Ollama, separate judging prompt.
- Hardware mode: CPU inference; no model data was sent to a cloud model API.
- Outcome: all seven rubric checkpoints passed on candidate 1.
- Memory: accuracy and coverage reminders were activated from earlier live failure events and appear in the report.
- Lesson provenance: model-generated teaching sections assembled into Markdown by the deterministic renderer. The fictional source note and example questions were supplied in the curated source pack; they were not retrieved from a real college website.

`lesson.md` is the actual passing output, copied without rewriting. `report.json` includes the generation input, model sections, rendered lesson, judge response and checkpoint verdicts. `rejection-log.md` is accurate: this particular completed run had no rejected candidate. Earlier development failures and interrupted runs are preserved locally in `outputs/`; offline retry behaviour is separately demonstrated under the original `examples` fixture.

The judge's evidence line IDs prove that selected text exists, not that the selected text logically justifies its conclusion. Some selected evidence is a heading. This is a known review limitation. The run does not establish population-level accuracy, learner comprehension or statistically measured improvement from memory. Check important lessons before publication.

The local run is complete. GitHub publishing, Google Docs/Notion publishing, the face-visible video and assessment-form submission have not been performed.

## Live deliberate-error test

`../examples/live-error-probe/report.json` records a separate real Qwen accuracy evaluation of a corrupted copy of this lesson. The injected sentence was `RAG guarantees every answer is correct.` The evaluator returned `pass: false` and selected that exact false sentence as evidence (line 79). The original passing lesson was not changed. This was an accuracy-only probe, not a full-rubric generation/regeneration run. The earlier attempt to use a full-rubric probe stopped on inconsistent coverage evidence; it did not authorise release.

Final local verification: twelve unit tests passed after the implementation changes.
