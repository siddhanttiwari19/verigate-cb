# verigate-cb — AI Risk Manager (Chargeback Evidence Responder)

Built for Razorpay Buildathon, Track 02: AI Risk Manager.

## What it does
Given an incoming chargeback dispute, the pipeline:
1. **Checks evidence integrity** — flags internally inconsistent evidence
   (e.g. a signature match with no delivery confirmation) before it's
   even scored.
2. **Scores winnability** — a logistic regression classifier outputs a
   calibrated probability, trained on delivery confirmation, signature
   match, IP/billing match, order history, and refund status.
3. **Explains the score** — every decision shows which evidence fields
   drove it, in plain language, not just a bare probability.
4. **Applies a dynamic threshold** — the confidence bar to auto-submit
   scales with the dispute amount. A ₹40,000 dispute needs a stricter
   bar than a ₹500 one.
5. **Drafts a representment letter** — cites specific evidence claims.
6. **Verifies the draft** — checks every cited claim against the actual
   evidence record. An unsupported claim rejects the whole response.
7. **Monitors for drift** — tracks whether live traffic is statistically
   diverging from what the model was trained on, and escalates
   everything if so, rather than silently degrading.
8. **Gates the action** — only (integrity-clean + high-confidence +
   verifier-approved + no drift) responses auto-submit. Everything
   else escalates to a human, and every decision is audit-logged.
9. **Captures feedback** — reviewers can record what actually happened
   to an escalated dispute, building a labeled dataset for retraining.

## Architecture
```
evidence --> integrity check --> scorer --> explainability
                                     |
                                dynamic threshold (by amount)
                                     |
                                  drafter --> verifier
                                     |            |
                                drift monitor      |
                                     +------+------+
                                            |
                                    decision gate --> audit log
```

## Run it locally
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app/data_gen.py
python -m app.orchestrator
```

## Run the API
```bash
cp .env.example .env           # then edit API_KEY to a real random string
uvicorn app.main:app --reload
```
Docs auto-generate at `http://localhost:8000/docs`.

Every data-facing endpoint requires an `X-API-Key` header matching your
`.env`'s `API_KEY`. `/health` is intentionally unauthenticated (load
balancers can't send custom headers).

Example:
```bash
curl -X POST http://localhost:8000/disputes/process \
  -H "X-API-Key: your-key-here" -H "Content-Type: application/json" \
  -d '{"dispute_id":"CB-001","reason_code":"product_not_received","amount_inr":15000,"evidence":{"delivery_confirmation":true,"signature_matches_cardholder":true,"ip_matches_billing_country":true,"prior_clean_order_count":5,"support_chat_exists":true,"refund_already_issued":false,"device_fingerprint_reused":false}}'
```

## Run with Docker
```bash
docker compose up --build
```
(Dockerfile written but not build-tested in this environment — no
Docker daemon was available. Run this yourself and flag anything that
breaks.)

## Run the tests
```bash
pip install pytest ruff
ruff check app/ tests/
pytest -v
```
17 tests covering the verifier, integrity checker, dynamic threshold,
drift monitor, and API auth — all passing as of this build.

## CI
`.github/workflows/ci.yml` runs lint + tests + a Docker build on every
push and PR to `main`. GitHub Actions picks this up automatically once
pushed — no setup needed on your end beyond having the file in the repo.

## Security notes
- API key required on every data-facing endpoint, compared in constant
  time (`hmac.compare_digest`) to avoid timing attacks.
- Per-IP rate limiting (30 req/min by default, configurable).
- No secrets committed — `.env` is gitignored, `.env.example` is the
  template. **Rotate the default `dev-only-change-me` key before any
  real deployment.**
- Docker image runs as a non-root user.
- Input validation via Pydantic on every API field (amount bounds,
  string length limits, enum-constrained outcome values).

## Honest limitations (say these in your pitch, don't hide them)
- The synthetic dataset includes 12% label noise, but real dispute
  outcomes are noisier and more structurally different than random
  flips — issuer discretion doesn't look like uniform noise.
- The drift monitor's baseline is computed from the same synthetic
  training set it evaluates against, so it hasn't been tested against
  a genuine distribution shift yet — that only becomes meaningful once
  real traffic flows through it.
- The drafting agent is template-based, not LLM-based, by design (for
  demo reliability with zero API keys required) — swapping in a real
  LLM call is a documented next step, not yet done.
- Rate limiting is in-memory and per-process — fine for one instance,
  needs a shared store (Redis) before running more than one worker.

## Track alignment (for the application form)
- Track: AI Risk Manager
- What it solves: chargeback evidence response with measured
  precision/recall, explicit false-positive cost, and a hallucination
  gate on money-facing output
- The bar it hits: explainable (per-decision factor breakdown +
  full audit log), bounded (amount-scaled threshold + verifier gate),
  one failure handled gracefully (verifier rejection -> escalation,
  not silent failure)
