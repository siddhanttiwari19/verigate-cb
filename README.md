# ChargebackSentinel — AI Risk Manager (Chargeback Evidence Responder)

Built for Razorpay Buildathon, Track 02: AI Risk Manager.

## What it does
Given an incoming chargeback dispute, the pipeline:
1. **Scores winnability** — a logistic regression classifier trained on
   dispute evidence (delivery confirmation, signature match, IP/billing
   match, order history, refund status) outputs a calibrated probability.
2. **Drafts a representment letter** — cites specific evidence claims.
3. **Verifies the draft** — checks every cited claim against the actual
   retrieved evidence record. A claim the evidence doesn't support gets
   the whole response rejected, not silently rewritten.
4. **Gates the action** — only (high confidence + verifier-approved)
   responses auto-submit. Everything else escalates to a human, and
   every decision is written to an append-only audit log.

## Why this beats a plain "LLM drafts a chargeback response" demo
Most entries in this track will have an LLM generate evidence text and
trust it. The verifier agent here is the actual novelty: it's a hard
gate between "the draft *claims* X" and "the evidence *proves* X."
That's the difference between a toy and something you could actually
point real money at — and it directly answers the judging criterion
"AI judgment: where you chose not to use one" (the gate is deliberately
non-LLM and rule-based, on purpose, because money-facing verification
shouldn't be probabilistic).

## Run it
```bash
pip install -r requirements.txt
python3 app/data_gen.py          # generates 500 synthetic disputes
python3 -m app.orchestrator      # trains scorer, runs batch, writes audit log
```
Outputs precision/recall/F1, a confusion matrix, false-positive cost in
INR, and revenue recovered vs. recoverable — the "honest metrics"
the track bar asks for.

## Honest limitation (say this in your pitch, don't hide it)
The synthetic ground-truth label is a deterministic function of the
same features the model trains on, so precision/recall on this data
looks unrealistically clean (P=0.92, R=1.0 in the current run). Real
chargeback outcomes are noisier — issuer discretion, partial evidence,
inconsistent reason codes. Before demo day:
- Add label noise to `data_gen.py` (flip ~10-15% of labels) so the
  eval is credible, not just internally consistent.
- If you can get real (anonymized) Razorpay test-mode dispute data,
  swap it in — same schema, same eval script.

## Next steps to make this buildathon-ready
1. **Swap `draft_agent.py` for a real LLM call** (Claude/GPT) once
   you're ready — the verifier doesn't care which agent produced the
   draft, so this is a drop-in change.
2. **Wire to Razorpay test-mode Disputes API** instead of synthetic
   data — same `evidence` dict shape, different source.
3. **Add a FastAPI layer** (`requirements.txt` already includes it)
   exposing `POST /disputes/{id}/process` so you have a live demo,
   not just a CLI batch run.
4. **Record the 5-min pitch around the verifier rejection case** —
   show a dispute where the draft over-claims and gets bounced to
   human review. That's your "what broke, and how you got out" story
   built into the product itself.

## Track alignment (for the application form)
- Track: AI Risk Manager
- What it solves: chargeback evidence response with measured
  precision/recall and an explicit false-positive cost
- The bar it hits: explainable (audit log per decision), bounded
  (confidence threshold + verifier gate), one failure handled
  gracefully (verifier rejection → escalation, not silent failure)
