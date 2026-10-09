# MemoryFirewall implementation plan

## Product outcome
MemoryFirewall is a full-stack developer console that makes agent memory inspectable, enforceable, and testable. The demo proves the core loop in under ten seconds: an unverified financial memory would trigger a refund in baseline mode, while the deterministic policy engine quarantines it, blocks the financial tool call, requests human approval, and turns the incident into a passing regression test.

## Implementation approach
- **Runtime:** One Express server on port 3000, bound to `0.0.0.0`, serving the Vite-built React client and REST APIs.
- **Persistence:** An explicit in-memory repository with seeded synthetic memories, runs, steps, tests, approval requests, and lightweight sessions. The repository shape mirrors the requested database schema so a database adapter can replace it later without changing API contracts.
- **Frontend:** React + Vite + TypeScript with client-side routing, reusable shell components, API helpers, toast feedback, loading/empty/error states, and route-aware pages.
- **Policy engine:** Deterministic rules for financial impact, expiry, scope, contradiction, and protected retrieval. Model reasoning is represented as “Gemma 4 / deterministic fallback”; enforcement never trusts model output alone.
- **Auth:** Demo-friendly sign-up/sign-in endpoints with hashed-password-style in-memory records, bearer session tokens, and a top-right account control. It is deliberately labeled synthetic/demo auth and is not production identity management.
- **Human approval:** Protected runs create an approval request. The UI can review, approve, or reject it; approval changes the request state and records an audit event while still never issuing a real refund.
- **Video:** A deterministic, self-contained motion-graphics onboarding video generated with SVG + FFmpeg, embedded in the How it works page. It explains the developer integration sequence: wrap memory writes, validate reads, enforce actions, replay decisions, and generate tests.

## Design system
- **Design movement:** Cosmic glassmorphism for developer infrastructure: translucent instrument panels floating over an orbital dark field, with restrained depth and purposeful motion.
- **Core principles:** Evidence before decoration; controlled urgency; compact observability; one clear action per state.
- **Color philosophy:** Ink navy and graphite create a calm observability surface. Electric lime means enforced safety and verified state. Coral is reserved for unsafe behavior. Amber signals uncertainty. Violet/cyan identify reasoning and system activity.
- **Layout paradigm:** A fixed left instrument rail plus an asymmetric workspace of glass panels, not a generic centered dashboard. Large hero copy anchors the left while evidence and action panels orbit the primary demo.
- **Signature elements:** Orbit rings and grid-stars in the background; a shield/node mark; thin lime “trace” connectors between memory and decision states; softly elevated glass cards with specular borders.
- **Interaction philosophy:** Every control causes a visible system event. Buttons use clear verbs, show pending state, and surface the backend result in a toast or panel. Dangerous actions require an explicit approval step; reset is always available.
- **Animation:** Slow background drift and pulse only. Panel entrances use short translate/fade. Trace nodes illuminate in sequence during protected runs. No animation obscures evidence or delays the demo.
- **Typography system:** Inter/system sans for UI hierarchy; JetBrains Mono/system monospace for IDs, API paths, YAML, and trace metadata. Headings are bold and compact, never oversized.
- **Brand essence:** A memory debugger and policy firewall for AI-agent developers — **inspectable, protective, pragmatic**.
- **Brand voice:** Direct and technical. Example lines: “One poisoned memory. Three wrong decisions.” and “Make agent memory testable like code.”
- **Wordmark & logo:** A custom inline SVG shield with an internal circuit node and orbit ring beside `MEMORY` + lime `FIREWALL`.
- **Signature brand color:** Electric lime `#c7ff5e`.

## Project structure
- `client/index.html` — Vite entry shell and metadata.
- `client/src/main.tsx` — React bootstrap.
- `client/src/App.tsx` — routes, app state, demo orchestration, auth, modals, and pages.
- `client/src/index.css` — complete cosmic glassmorphism design system and responsive layout.
- `server/index.ts` — Express server, repository, deterministic policy engine, API routes, static serving, and dev Vite middleware.
- `public/manus-routes.json` — page route manifest required by Webdev.
- `public/assets/memoryfirewall-onboarding.mp4` — embedded developer onboarding video.
- `scripts/render-onboarding-video.py` — reusable SVG scene generator and FFmpeg assembly source.
- `app.config.ts` — durable project logo metadata.
- `README.md` — product, API, setup, demo script, limitations, and roadmap.

## Required behavior preserved from the specification
The main demo, memory ledger/passport, replay timeline, regression tests, settings/integrations content, REST contract, synthetic disclaimer, and deterministic enforcement rules remain in scope. New scope adds sign-up/sign-in, human approval, a reliable Run demo action, cosmic glass UI, a How it works guide, and an embedded onboarding video.
