# Design and reasoning

## Plan and acceptance conditions

1. Define the learner: Indian class-12 graduate, limited English, no AI knowledge.
2. Curate a narrow factual source pack and use a familiar college scenario.
3. Define a fixed binary rubric before generation.
4. Separate content generation, judging and deterministic release control.
5. Feed explicit failures and the prior candidate into bounded regeneration.
6. Persist failures and use repeated patterns to strengthen future prompts.
7. Test incorrect content, invalid verdicts, exhausted retries and persistent memory.
8. Perform a live run, inspect evidence and publish the resulting artifacts.

The local model portion of step 8 completed on 7 November 2026. Publishing and recording still require the submitter's accounts and face-visible walkthrough. See `final/RUN-NOTES.md` for the observed run and its limits.

## Component responsibilities

`Ollama` adapts model calls. Generator and judge receive separate system prompts and can use different models. Responses are constrained using JSON schemas. The judge selects evidence from enumerated lesson line IDs; the adapter resolves each ID to original text. This avoids asking a small model to reproduce punctuation and Markdown exactly. It does not guarantee that the selected line supports the verdict. `run` controls state transitions and release. `validate_verdict` enforces exact checkpoint coverage, boolean types and source-text evidence. SQLite stores rejection events. Files preserve the complete audit trail. Keeping this in plain Python makes control flow easy to review and test without framework abstractions.

## Binary rubric

| Check | Pass condition | Why it matters |
|---|---|---|
| Accuracy | All substantive claims agree with curated facts; no correctness guarantee or normal retraining claim | A readable false lesson is harmful |
| Coverage | Definition, purpose, preparation, retrieval, context, generation and two limitations | Learner needs a complete first mental model |
| Language | Simple English, manageable sentences and no unnecessary difficult language | Fits the stated learner |
| Example | Consistent question, evidence, answer, source and missing-evidence behaviour | Shows the actual information flow |
| Jargon | Every specialist term used has a plain explanation | Prevents assumed background knowledge |
| Flow | Familiar problem through recap in a coherent order | Helps the learner build knowledge step by step |
| Practice | Exercise and short knowledge check, with correct answers | Gives the learner a chance to apply the idea |

These are hard pass/fail decisions with no weighted average. Language and flow remain qualitative judgments; a boolean output does not make them perfectly objective. A future validation study should compare them against labels from instructors and representative learners. Sentence length alone is not a reliable comprehension test.

## Grounding and security

The source pack is curated context. The original RAG paper is listed for provenance: https://arxiv.org/abs/2005.11401 . The application does not fetch or verify URLs at runtime, so citations are not evidence of a live retrieval step. College and shop examples are explicitly fictional.

The judge is told to ignore instructions in lesson text. This mitigates but does not solve prompt injection. Exact-quote checks cannot establish that a quote supports a verdict. A stronger system would add independent factual checks, adversarial test cases and human audits. Do not use confidential learner data with an unapproved endpoint.

## Self-evolution trade-off

Arbitrary auto-editing of the judge risks rewarding weaker standards. Instead, repeated checkpoint failures activate a fixed repair reminder. The rubric stays unchanged and its version/hash are recorded. Demo memory never contaminates live memory. Advice is topic-scoped, bounded to seven rules and cannot copy untrusted model text. The current mechanism learns which reminders to activate, not new factual knowledge. It may not improve outcomes; measure that before making improvement claims.

## Failure and resource policy

At most three candidates. Each candidate uses one generation call and one judge call, plus at most one judge repair call for invalid verdicts: nine calls maximum. The repair receives the validation error and unchanged lesson; all original checks remain required. Raw judge responses are preserved, including invalid quotes. A second invalid verdict stops release. Each request has a configurable timeout, defaulting to 900 seconds. Transport failures stop immediately. Outputs are local and per-run. A passing lesson alone is exported to `lesson.md`; failed candidate texts remain in `report.json` for audit. For local operation, serial execution and SQLite are sufficient; concurrent production workers need stronger transactional orchestration and scheduling.

## Validation and next steps

Twelve tests establish bounded control flow, rejection of malformed booleans and fabricated evidence, one bounded verdict repair, non-release on failure, persistence, isolation and correct resolution of evidence line IDs. They do not measure live semantic judge accuracy. The offline deliberate-error demo establishes orchestration only.

The recorded successful run used Gemma 3 4B for generation and Qwen 3 8B for judging on CPU. Every checkpoint passed on its first candidate. Earlier Gemma-as-judge runs showed both false rejections and missed content problems; these led to selecting a different judge, not weakening the rubric. This experience reinforces the need to compare judge decisions with a human-labelled set containing subtle factual errors, unexplained terms, inconsistent examples and prompt injection. Track false acceptance, false rejection, attempts to pass, latency and quality before/after memory activation. One passing run is not proof of reliable judging or measured memory improvement. Human review remains appropriate for publication.
