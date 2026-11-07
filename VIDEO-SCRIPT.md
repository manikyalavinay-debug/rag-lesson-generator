# 18-minute recording plan

Use Loom or a similar recorder with your face visible. Rehearse first. Use your own words and explain only claims you can demonstrate. Do not narrate the fixture as a real model evaluation.

| Time | Show | Explain |
|---|---|---|
| 0:00-1:30 | README and learner brief | Who the lesson serves; why an unchecked first draft is insufficient |
| 1:30-3:30 | DESIGN and rubric.json | Seven binary checkpoints; all must pass; evidence required |
| 3:30-5:30 | app.py run and adapters | Separate generator, judge and controller; two retries maximum |
| 5:30-8:30 | Terminal: run live models | Use an already installed generator and judge; state their exact names; explain source pack and memory inputs |
| 8:30-10:30 | Live report and released lesson | Inspect every decision; show why any rejection happened; if rejected, explain the failure honestly |
| 10:30-12:30 | `python app.py --demo` and its report | Explicitly label offline fixture; locate the injected false guarantee, accuracy failure and repaired candidate |
| 12:30-14:00 | `python -m unittest -v` | Non-release after exhaustion; schema errors; persistence and memory isolation |
| 14:00-15:30 | Three demo runs using one fresh demo memory file | Third run receives accuracy reminder after failures in two distinct runs |
| 15:30-17:00 | Final lesson | Explain the college example as if teaching the target learner |
| 17:00-18:00 | DESIGN limitations and submission links | Judge uncertainty, bounded evolution, future human-labelled evaluation |

If a live run takes longer than the recording window, prepare a completed run to inspect but identify it clearly as previously recorded. Show a fresh live invocation too. Do not cut footage to imply that a rejected lesson passed.

Before recording: increase terminal text size, hide unrelated windows, check microphone/camera, close secret-bearing files, and verify the video link is viewable by the reviewer.

## Prepared live evidence

The completed real run is under `final/` and `examples/live/`. It used Gemma 3 4B to generate and Qwen 3 8B to judge. It passed on its first candidate; do not narrate earlier interrupted development attempts as retries within that successful run. `examples/DEVELOPMENT-LOG.md` explains the actual development sequence and fixes.

To show the real accuracy evaluator examining a corrupted copy of the passing lesson:

```powershell
python -u error_probe.py --lesson final/lesson.md --model qwen3:8b
```

This is an accuracy-only evaluation probe, not a full-rubric pipeline run. It appends a false correctness guarantee, preserves the modified input and verdict, and never releases that modified lesson. Inspect its report before claiming that it caught the error. For a full live generation/evaluation/regeneration demonstration instead, add `--inject-error` to `app.py`; that takes longer on this CPU-only machine. The offline `--demo` run remains a separate, scripted control-flow demonstration.
