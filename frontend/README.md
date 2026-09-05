# verigate console — frontend

The UI for verigate-cb, designed as a risk-ops review console rather than a
generic dashboard: the whole interface exists to make one judgment call
legible — should a human trust this AI's chargeback decision, or override it.

## What's here
- `/` — landing page. One GSAP-driven hero reveal, then a single scroll-story
  section (`#gate`) that literalizes the verifier check: a draft letter's
  claims get checked one by one as you scroll, ending in a stamp.
- `/console` — the actual review tool. A dispute queue (left) and full case
  detail (right): confidence, per-factor explainability, evidence checklist,
  the drafted letter, and a verdict stamp — approved (green) or rejected
  (rust), matching your backend's `verifier_approved` field exactly.

## Design system
- Colors, fonts, and the full reasoning are documented inline in
  `app/globals.css` and in the original design brief given during build.
- Fonts: Fraunces (display/headlines), Inter (UI chrome), JetBrains Mono
  (every number, ID, and evidence value — deliberate, not decorative).

## Run it
```bash
npm install
npm run dev
```
Open `http://localhost:3000` for the landing page, `http://localhost:3000/console`
for the review tool.

## Data
Currently wired to `lib/mockData.ts`, shaped to match your FastAPI backend's
`/disputes/process` response exactly (same field names, same decision enum).
To connect it to your real backend instead of mock data, replace the
`mockDisputes` import in `app/console/page.tsx` with a `fetch()` call to
`http://localhost:8000/disputes/process` (remember to send the `X-API-Key`
header your backend expects) — the response shape needs no transformation.

## Build
```bash
npm run build
```
Verified clean in this environment except for one sandbox-only limitation:
this build environment blocks outbound requests to fonts.googleapis.com, so
`next/font/google` can't fetch fonts here. That's a network restriction of
the build sandbox, not a bug in the code — it will fetch normally on your
machine or any real deploy host (Vercel, etc.) with standard internet
access. Confirmed by temporarily stubbing the fonts and rebuilding: the rest
of the app (both routes, all components, TypeScript, ESLint) compiles clean.
