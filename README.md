# Self-evaluating lesson generator

A beginner lesson is released only when every fixed checkpoint passes. Any failed checkpoint sends concrete reasons into regeneration. Two retries maximum; failed or malformed evaluations never produce a released lesson.

**Delivery status:** A real local model run completed successfully on 7 November 2026: `gemma3:4b` generated the lesson and `qwen3:8b` judged all seven checkpoints as passing. Read `final/lesson.md` and `final/report.json`. The final run also received accuracy and coverage reminders learned from earlier live failure events. This is one observed success, not a measurement of judge reliability. Twelve tests pass. The offline demo remains a scripted fixture, clearly separate from live results. Publishing and the face-visible recording remain account-bound steps.

## Quick start (PowerShell, Python 3.10+)

No Python packages are required.

```powershell
cd rag-assessment
python -m unittest -v
python app.py --demo
```

Tests intentionally exercise failures and may print `ERROR`, `FAIL`, or `REJECTED`. A final unittest summary of `OK` means the tests passed. Those messages are different from an error in a normal live run.

The demo intentionally appends a false guarantee to attempt 1. Its fixture judge rejects it. Attempt 2 removes it. Inspect `outputs/<run-id>/report.json` for complete candidate texts, inputs, verdicts and evidence; `rejection-log.md` explains failures and repairs; `lesson.md` exists only on success. Each run has a unique directory, so an earlier passing lesson cannot be mistaken for a later failed run.

## Run with real models

Install Ollama using its official instructions: https://ollama.com/download . Choose models your hardware can run. The names below are examples, not a guarantee of suitability or availability. Pulling models downloads large files; this project does not do that automatically.

```powershell
ollama pull qwen3:8b
ollama pull gemma3:4b
python app.py --model qwen3:8b --judge-model gemma3:4b
```

Ensure Ollama is running locally. Each model request allows 900 seconds (15 minutes) by default. For slower computers, pass `--timeout 1800` to allow 30 minutes per request, or use a smaller installed model. Requests do not have hidden transport retries. A transport error stops the run and is recorded; rerun after resolving it. Exit code 0 means passed, 1 means rejected/error. Invalid CLI arguments also exit nonzero.

The adapter uses Ollama's documented `/api/chat` interface with non-streaming JSON responses: https://github.com/ollama/ollama/blob/main/docs/api.md . No API key is required for local models. Live evaluation is still fallible, even when it passes every check.

On a CPU-only computer, using the smaller installed model for both roles avoids loading the larger model:

```powershell
python -u app.py --model gemma3:4b --judge-model gemma3:4b --timeout 1800
```

Separate prompts do not make the same model an independent judge. Record this limitation in your walkthrough. For a deliberate-error demonstration with real calls, add `--inject-error`. This appends a known false correctness guarantee to candidate 1; the evaluator must reject it. An actual recorded evaluation, not the option alone, establishes whether the judge caught it.

Generation now returns required teaching sections rather than a free-form lesson string. A deterministic renderer assembles the source note, question, cited answer, missing-evidence example, practice and recap into Markdown. The judge still checks whether those fields teach the correct content; schema presence alone is insufficient.

## Pipeline

```text
Topic + curated facts + fixed rubric + scoped memory advice
                         |
                      Generate <-------------------+
                         |                         |
                    Judge all checks               |
                         |                         |
                Validate verdict schema            |
                 /         |          \            |
             malformed   all pass    any fail       |
                |          |          |            |
              ERROR     RELEASE   Log to SQLite    |
                                      |            |
                               retries remain? ----+
                                      |
                               no: REJECTED
```

The learner starts from zero. The fixed rubric covers accuracy, coverage, language, examples, jargon, flow and practice. Each check is boolean; release requires all seven passes. Live judge responses use a JSON schema with all checkpoint names required. Evidence is selected from numbered lesson lines (or `MISSING` for a failure), then resolved by the program to original text and validated. The selected line must exist, but that alone cannot prove it supports the judge's reasoning. Candidate drafts and initial evaluations are saved as soon as they arrive, even before a final report exists.

## Persistent memory and self-improvement

Failures persist in SQLite across runs. A checkpoint failing in **two distinct runs** activates an approved prompt reminder on subsequent runs. Repeated failures in one run do not meet the threshold. Advice is isolated by topic and demo/live mode, and is included in the audit report. Run the demo three times with the same memory path to see the third run receive advice.

This is deliberately bounded self-evolution: historical evidence sharpens generation prompts through a fixed mapping. The system cannot lower a rubric threshold, adopt arbitrary failed-output instructions, or silently rewrite its own judge. It does not fine-tune weights or demonstrate statistically proven quality improvement. It records model-reported changes alongside full candidate texts so reviewers can verify repairs themselves.

## Other topics

```powershell
python app.py --topic "Your topic" --sources path/to/curated-source-pack.json
```

Supply a JSON source pack with a matching `topic`, `facts`, and `references`. The default pack is for Introduction to RAG. The system is a lesson generator about RAG; it is not itself a production document-retrieval service. Generalise factual checks and review topic-specific coverage before using the rubric for a different subject. Demo mode supports only the included RAG fixture.

## Submission files

- `DESIGN.md`: planning, rubric rationale, trade-offs and limitations.
- `lesson.md`: curated sample lesson for review and fixture testing.
- `VIDEO-SCRIPT.md`: 18-minute face-visible walkthrough plan.
- `SUBMISSION.md`: exact publishing and recording checklist.
- `examples/live/`: actual successful live lesson, full report and rejection log.
- `examples/live-error-probe/`: a real Qwen accuracy check rejecting an injected false guarantee, with the exact rejected sentence as evidence.
- `final/`: convenient copies of the successful live deliverables.
- `examples/20261107T075601Z-56e4cf92/`: original recorded offline demo.

Do not describe an offline fixture run as live model generation. Use the real lesson in `final/lesson.md` for the final document. No GitHub repository, Google Doc, Loom video, or assessment form has been published by this project.
