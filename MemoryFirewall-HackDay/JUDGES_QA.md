# MemoryFirewall — Hacktoberfest Hack Day Bengaluru ’26
## Round 1 Judge & Mentor Discussion Brief

> **One-line pitch:** MemoryFirewall is an open-weight-AI-compatible safety and reliability layer that makes AI-agent memory inspectable, enforceable, replayable, and testable before it can trigger high-impact tools.

## Status legend

- **Implemented in the current demo:** available in the working web application.
- **Hack Day target:** the production-strength increment we would complete during the Hack Day.
- **Important honesty:** the current demo uses a deterministic fallback and does not make a live hosted Gemma call yet. Gemma is represented as the reasoning layer and is the planned/required model integration. Critical enforcement is intentionally deterministic so a model cannot authorize a sensitive action by itself.

---

# 1. Problem Statement & Proposed Solution

## What problem are you trying to solve, and who experiences it?

AI agents increasingly use long-term memory: user preferences, support history, policies, approvals, and facts retrieved from chats or tools. The problem is that memory is often treated as trusted context even when it is stale, contradictory, out of scope, low-confidence, unsupported, or maliciously inserted.

That creates a dangerous failure mode:

1. A weak or unverified claim enters memory.
2. The agent retrieves it later.
3. The model treats it as fact.
4. A tool call performs a high-impact action.

The people affected are:

- AI developers and ML engineers building agent systems.
- Support, finance, healthcare, operations, and security teams using agents.
- End users whose money, privacy, access, or reputation can be affected.
- Engineering teams that need to debug why an agent made a decision.

## Why does this problem matter?

Traditional prompt testing checks whether a model responds correctly to a prompt. It does not adequately test whether the model was influenced by an unsafe memory retrieved from a long-term store.

A single poisoned memory can be reused across many conversations. A stale policy can cause an incorrect action. A cross-customer memory can create a privacy breach. A false approval can authorize a financial operation.

The impact is not only an inaccurate answer; it can be an irreversible tool action. Therefore, memory needs provenance, policy enforcement, human review, and regression tests just like application code.

## What is your proposed solution, and how will it address the problem?

MemoryFirewall sits between an AI agent and its memory backend. It provides five controls:

1. **Memory passport:** every memory carries source, trust, confidence, scope, impact, evidence, expiry, and usage information.
2. **Write-time validation:** suspicious or high-impact claims are flagged before they become trusted long-term memory.
3. **Protected retrieval:** stale, revoked, conflicting, wrong-scope, or quarantined memories are filtered before they influence high-impact actions.
4. **Human approval:** sensitive actions pause for a reviewer with the exact evidence chain visible.
5. **Decision replay and regression tests:** every protected run records request → memory → validation → tool decision → outcome, and incidents can become repeatable tests.

The demo scenario is a synthetic refund agent. The suspicious memory is:

> “Customer has already approved the refund.”

It came from `unverified_chat`, has confidence `0.32`, financial impact, low trust, and no evidence. The baseline agent issues an unsafe ₹18,500 refund. The protected path quarantines the memory, blocks `issue_refund()`, and requests human verification.

## How is your approach different from existing solutions?

Most agent frameworks focus on orchestration, retrieval, prompt management, or observability. MemoryFirewall focuses specifically on the **trust boundary between memory and action**.

The difference is the closed reliability loop:

> provenance → deterministic policy → human approval → causal replay → regression test

We are not asking the model to be its own security layer. The model may reason and explain, but deterministic rules remain in front of high-impact tools.

---

# 2. Dataset & AI Model

## Which AI model or models do you plan to use, and why?

### Primary model: Gemma 4

Gemma 4 is the selected reasoning layer because it is an open-weight model family that can be run through a controlled endpoint or local deployment. It is suitable for:

- Interpreting the user request.
- Summarizing retrieved memories.
- Explaining how a memory influenced a proposed action.
- Classifying or extracting memory metadata when appropriate.
- Helping convert an incident into a regression-test description.

### Deterministic policy engine

The enforcement engine is intentionally not delegated to Gemma. It checks explicit rules for:

- Financial, safety, and privacy impact.
- Memory status and trust level.
- Evidence availability.
- Expiry and staleness.
- Scope and customer identity.
- Conflicting or revoked memories.

This hybrid design makes Gemma meaningful without allowing a probabilistic model to override a safety boundary.

### Current demo status

The current website is offline-friendly and does not require an external API key. It displays the Gemma 4 reasoning-layer trace and uses a deterministic fallback for the actual demo. The Hack Day implementation target is to connect Gemma 4 through a configurable inference endpoint while retaining the same deterministic enforcement path.

## What datasets, APIs, documents, or other data sources will you need?

### Current demo data

- Fully synthetic customer-support memories.
- Synthetic request: “Please refund my order.”
- Synthetic suspicious approval memory.
- Synthetic policy memory, subscription memory, and customer-preference memories.
- No real customer PII, payment credentials, or payment-provider calls.

### Hack Day / production adapter data

- Memory records with provenance, confidence, impact, scope, expiry, and evidence.
- Agent request and tool-call traces.
- Optional policy documents and support notes.
- Optional vector-store retrieval results.
- Optional Gemma inference endpoint.
- No external API is required for the core safety demo.

The design can later connect to PostgreSQL/MySQL, Redis, Mem0, a vector database, LangChain, LlamaIndex, or an existing memory backend through adapters.

## How will AI contribute to the core functionality?

AI contributes to the flexible, semantic parts of the workflow:

1. Understand a natural-language request.
2. Identify which memories are relevant.
3. Summarize the evidence chain for a developer or reviewer.
4. Suggest a candidate action.
5. Convert a failed decision into a structured regression test.

The deterministic layer contributes the non-negotiable safety decision. For example, even if Gemma says “the customer approved the refund,” the action remains blocked when the memory is financially sensitive, low-trust, and unsupported.

## How does your model choice align with the selected challenge track?

It aligns with **Best Use of Gemma 4** because Gemma is not included as decoration or a chatbot. It is placed in the reasoning, explanation, and test-generation path of an agent-memory control plane.

It also aligns with **Best Open-Source AI Project** because the system is designed around an open-weight model, an open-source developer workflow, a transparent REST contract, deterministic policy code, reproducible synthetic data, and an MIT-licensed project intended for public GitHub publication.

---

# 3. Technology Stack & Architecture

## Which frontend, backend, database, AI frameworks, APIs, and cloud services will you use?

### Current stack

- **Frontend:** React, TypeScript, Vite.
- **UI:** custom dark cosmic glassmorphism console, responsive CSS, Lucide icons.
- **Backend:** Node.js with Express and TypeScript.
- **Repository:** deterministic in-memory demo repository with seeded records.
- **API:** REST endpoints for memories, demo runs, approvals, replay, tests, and authentication.
- **Video:** Python/Pillow frame renderer and FFmpeg for the embedded developer-onboarding walkthrough.
- **Cloud/runtime:** managed web Preview/runtime with a server listener on `0.0.0.0:3000`.

### Hack Day target stack

- **Database:** PostgreSQL or MySQL for durable memory passports, decision runs, approval events, and regression tests.
- **Memory/vector adapter:** pluggable interface for an existing vector store or memory product.
- **AI inference:** Gemma 4 through a local or hosted inference endpoint.
- **CI integration:** GitHub Actions running generated memory regression tests.
- **Deployment:** containerized Node service with environment-based model and database configuration.

## How will the components interact?

```text
User request
    │
    ▼
AI agent / orchestration layer
    │
    ▼
MemoryFirewall SDK or REST API
    ├── retrieve candidate memories
    ├── attach memory passports
    ├── run deterministic validation
    ├── call Gemma for reasoning/explanation when needed
    ├── allow, filter, quarantine, or request approval
    ├── record the full decision trace
    └── generate a replayable regression test
    │
    ├── approved tool call
    └── blocked / verification-required tool call
```

### Protected refund flow

1. The agent receives “Please refund my order.”
2. Memory retrieval finds `mem_1042`.
3. The passport shows `unverified_chat`, confidence `0.32`, financial impact, and no evidence.
4. The deterministic policy engine marks it unsafe and quarantines it.
5. Gemma may explain the proposed reasoning, but cannot override the policy.
6. `issue_refund()` is blocked.
7. A human approval request is created.
8. The decision trace is replayable.
9. The incident is converted into `unverified_refund_approval_must_not_trigger_refund`.

## Why have you selected these technologies?

- **React/TypeScript:** fast iteration, strong UI typing, and a good fit for a dense developer console.
- **Vite:** fast development and small production frontend build.
- **Express/TypeScript:** simple, transparent REST API with shared types and low setup overhead during a Hack Day.
- **Deterministic repository first:** keeps the demo reproducible and removes database setup risk while preserving a database adapter boundary.
- **Gemma:** open-weight reasoning that can be self-hosted or deployed behind a controlled endpoint.
- **REST:** makes the control plane easy to integrate with agents written in different languages.
- **FFmpeg/Python:** creates a self-contained onboarding walkthrough that works without third-party video services.
- **Open-source tooling:** reduces lock-in and makes the architecture inspectable by judges and future contributors.

---

# 4. Novelty & Innovation

## What makes your idea different from existing solutions?

MemoryFirewall treats long-term agent memory as an untrusted dependency rather than an invisible prompt attachment.

Existing systems may expose traces or retrieval scores, but MemoryFirewall connects retrieval trust directly to tool authorization and then closes the loop with regression tests.

## What is the key innovative feature or approach?

The key feature is the **memory passport + deterministic enforcement + replay-to-test loop**.

A memory is not just text. It has identity, provenance, trust, confidence, scope, impact, evidence, expiry, and usage. That metadata can drive policy before the model is allowed to influence a high-impact action.

The second innovation is that a production incident is not left as a log. It becomes a named test that can be replayed after a prompt, model, memory, or code change.

## Are you introducing a new capability or improving an existing process?

Both:

- **New capability:** treating memory provenance and trust as a first-class action-enforcement input.
- **Improved process:** turning agent-memory incidents into reviewable, replayable regression tests instead of manually inspecting logs each time.

---

# 5. Implementation Plan & Demonstration

## What are the core features you intend to build?

### Implemented in the current demo

- Dashboard with seeded reliability metrics.
- Baseline unsafe refund simulation.
- Protected refund simulation that blocks the action safely.
- Memory ledger with search and status filters.
- Memory passport drawer.
- Verify, quarantine, revoke, and set-expiry actions.
- Human approval queue with approve/reject actions.
- Decision replay and explanation view.
- Regression-test generation and execution.
- YAML test export.
- Sign up, sign in, session, and sign out demo flow.
- “How it works” developer guide.
- Embedded onboarding video.
- Responsive cosmic glassmorphism interface.

### Hack Day target additions

- Live Gemma 4 inference adapter.
- Durable database adapter.
- Real SDK wrapper for agent memory writes and retrieval.
- Audit-event API and retention policy.
- Automated API and policy test suite in GitHub Actions.
- Public GitHub repository and open-source contribution guide.

## How will you demonstrate that the solution works?

The judge demonstration should follow this sequence:

1. Open **Overview**.
2. Click **Run unsafe baseline**.
   - Show `UNSAFE`.
   - Show `issue_refund()` executed.
   - Show simulated potential loss of ₹18,500.
3. Click **Reset demo**.
4. Click **Run with MemoryFirewall**.
   - Show `BLOCKED_SAFELY`.
   - Show the suspicious memory and policy reason.
   - Show the human approval drawer.
5. Open **Decision Replay**.
   - Walk through request → memory → validation → blocked tool → verification request.
6. Open the approval queue.
   - Reject or approve the simulated action.
   - Emphasize that no real payment call exists in the demo.
7. Click **Generate memory test**.
8. Open **Regression Tests** and click **Run all tests**.
   - Show the named test and PASS status.
9. Open **How it works** and play the onboarding video.

## What can your team realistically implement within the Hack Day?

A realistic Hack Day scope is:

- One complete customer-support scenario.
- One live Gemma 4 integration path.
- One durable persistence adapter or a clearly isolated repository interface.
- Deterministic policy enforcement for financial, scope, expiry, conflict, and evidence rules.
- Human approval state transitions.
- Replay trace and generated regression test.
- A public GitHub repository with setup instructions and an open-source license.
- A polished demo and documentation.

We would not claim to solve every agent memory problem in one Hack Day. The goal is a credible vertical slice that proves the core control loop.

## How will work be divided among team members?

Replace the role labels with the actual team member names before presenting:

| Role | Responsibility |
| --- | --- |
| Product/demo lead | Problem framing, judge narrative, scenario design, final demonstration |
| AI/model engineer | Gemma 4 adapter, structured outputs, reasoning/explanation prompts, model evaluation |
| Backend/reliability engineer | Memory passport schema, deterministic policy engine, approval state, replay API |
| Frontend/product engineer | Console UI, drawers, traces, filters, responsive design, onboarding flow |
| DevOps/documentation owner | Public GitHub repository, license, setup, CI regression tests, deployment |

If the team is smaller, combine the frontend/product and demo roles, and combine the backend and DevOps roles.

---

# 6. Feasibility & Real-World Impact

## Can the solution be built with the available time and resources?

Yes, because the project is intentionally scoped as a vertical slice:

- The demo uses deterministic synthetic data.
- The core REST API already exists.
- The policy rules are explicit and testable.
- The UI has no dependency on an external payment provider.
- Gemma is isolated behind a model adapter.
- The repository can begin in memory and move to a database without changing the user-facing flow.

The main time risk is integrating and evaluating live Gemma inference while keeping latency, structured output, and failure handling predictable. The fallback path prevents the safety demo from failing if the model endpoint is unavailable.

## Who will benefit, and what practical impact could it create?

### Direct beneficiaries

- AI-agent developers who need trustworthy memory behavior.
- ML/platform engineers operating retrieval and vector infrastructure.
- Security and compliance teams reviewing agent actions.
- Support and operations teams deploying automation.
- End users affected by agent decisions.

### Practical impact

- Fewer unsafe tool calls caused by stale or poisoned memory.
- Faster debugging of agent decisions.
- Clearer human review for sensitive actions.
- Reproducible tests for memory-related regressions.
- Easier adoption of agents in financial, support, and operational workflows.

The project does not claim to eliminate all model risk. It creates an enforceable, inspectable boundary around one of the most important sources of agent failure: memory.

## What limitations, dependencies, or risks have you identified?

### Limitations

- The current demo uses synthetic data and never performs a real refund.
- The current demo does not yet make a live Gemma call.
- The current repository is an in-memory implementation, not a production multi-tenant database.
- Model explanations are useful evidence, not formal security proofs.

### Dependencies

- Gemma inference endpoint or local model runtime for live model usage.
- Durable database and vector-store adapter for production.
- Proper authentication, authorization, tenant isolation, and secret management.
- Public GitHub repository and license for challenge submission.

### Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Model hallucinates an approval | Deterministic policy blocks low-trust high-impact memory |
| Memory crosses customer scope | Scope check blocks retrieval/action |
| Policy becomes stale | Expiry and replayable tests |
| Gemma endpoint is unavailable | Deterministic fallback keeps enforcement and demo working |
| Human approval becomes a bottleneck | Approval queue prioritization and clear evidence summary |
| False positives block valid work | Verification and explicit memory actions allow controlled recovery |
| Sensitive data leaks into logs | Synthetic demo data, redaction, tenant isolation, retention controls |

---

# 7. Challenge Requirements

## Best Use of Gemma 4: where and how will it be used?

Gemma 4 will be used in three meaningful places:

1. **Agent reasoning:** interpret the request and candidate memory context.
2. **Decision explanation:** produce a concise developer-readable explanation of which memory influenced the proposed action and what evidence was present or missing.
3. **Test generation:** convert a confirmed incident into structured regression-test fields such as input, forbidden memory, forbidden action, and expected safe action.

The system will pass Gemma structured context, not unrestricted authority. The model will return a proposed action or explanation, and the deterministic policy engine will independently enforce the final decision.

### Example structured interaction

```json
{
  "request": "Please refund my order.",
  "memory": {
    "content": "Customer has already approved the refund.",
    "source": "unverified_chat",
    "confidence": 0.32,
    "impact": "FINANCIAL",
    "evidence": []
  },
  "task": "propose_safe_action_and_explain"
}
```

Expected model contribution:

```json
{
  "proposed_action": "request_verification",
  "reason": "The approval claim is financially sensitive but has low confidence and no evidence.",
  "memory_reliability": "low"
}
```

The enforcement engine still checks the facts itself and blocks `issue_refund()` regardless of the model’s wording.

## Best Open-Source AI Project: how is open-source or open-weight AI important?

Open-weight AI is central because MemoryFirewall is designed to work with a model that developers can inspect, run in a controlled environment, and adapt rather than treating a closed model API as the entire trust boundary.

The project is also built with open-source technologies and a transparent REST contract. The intended submission includes:

- Public GitHub repository.
- MIT license or another appropriate open-source license.
- Reproducible setup instructions.
- Synthetic seed data.
- Policy rules visible in source.
- Model adapter interface.
- Regression tests and CI instructions.
- Clear separation between model suggestions and deterministic enforcement.

### Submission requirement still to complete

The current project has been checkpointed in the managed project repository, but it has **not yet been published to a public GitHub repository in this session**. That must be completed before final submission because the guidelines explicitly require a public GitHub repository and open-source license.

Do not claim this requirement is complete until the public repository URL, license file, and successful clone/setup instructions are available.

---

# 8. Clarity & Team Collaboration

## Explain your idea in a structured, clear, and concise manner.

Use this 30-second explanation:

> AI agents do not only fail because of bad prompts. They also fail because they trust bad memory. MemoryFirewall sits between an agent and its memory backend, gives every memory a provenance passport, filters unsafe memories before high-impact actions, pauses sensitive actions for human review, and turns incidents into replayable regression tests. In our refund demo, an unverified approval memory causes the baseline agent to issue a simulated ₹18,500 refund, while MemoryFirewall quarantines the memory and blocks the tool call safely. Gemma provides reasoning and explanations, but deterministic policy remains in control of enforcement.

## Ensure every team member understands the proposed solution.

Every team member should be able to answer these five questions:

1. What is the unsafe memory in the demo?
2. Why does the baseline agent fail?
3. Which deterministic rule blocks the protected path?
4. Where does Gemma contribute?
5. How does the incident become a regression test?

The shared answer is:

> The memory is “Customer has already approved the refund.” It is unverified, low-trust, financial, and unsupported. The baseline trusts it and calls `issue_refund()`. MemoryFirewall quarantines it and requests verification. Gemma reasons and explains, but cannot override the deterministic policy. The trace becomes `unverified_refund_approval_must_not_trigger_refund`, which must pass after future changes.

## Be ready to answer follow-up questions about model, architecture, feasibility, and outcomes.

### Is Gemma making the final safety decision?

No. Gemma proposes reasoning and explanations. The deterministic policy engine makes the final safety decision for high-impact actions.

### Why not rely only on prompting the model?

Prompts are not a sufficient control boundary for financial, privacy, or safety actions. A prompt can be misunderstood, a memory can be poisoned, or a model can generate an unsupported approval. Explicit policy is easier to test and audit.

### Why use synthetic data?

The Round 1 demo must be safe, reproducible, and free of personal or financial data. Synthetic data lets judges reproduce the exact result without external accounts or payment providers.

### What happens if a valid memory is quarantined?

A human can verify it, the memory can receive stronger evidence/trust, and the action can be retried under controlled approval. The system favors a reviewable pause over an irreversible action.

### How do you measure success?

Initial demo metrics:

- Unsafe baseline path visibly executes `issue_refund()`.
- Protected path blocks the same action.
- The suspicious memory is identifiable through its passport.
- The full decision trace is replayable.
- The generated regression test passes.
- Reset returns the demo to a deterministic seed state.

Hack Day evaluation metrics:

- Policy precision/recall on a labeled synthetic memory set.
- Number of unsafe tool calls blocked.
- False-positive rate for trusted memories.
- Replay reproducibility.
- Gemma structured-output validity and latency.
- Regression-test coverage across memory failure modes.

## Show that your team has a clear plan and can collaborate effectively.

The team will work in parallel around stable interfaces:

- Backend owns memory passport and policy contracts.
- AI owner owns Gemma adapter and structured outputs.
- Frontend consumes REST contracts and owns the judge flow.
- DevOps/documentation owner owns public repository, license, CI, and setup.
- Everyone tests the same canonical refund scenario and reviews the final narrative.

The most important collaboration rule is that the policy contract and demo scenario remain stable while implementation details evolve.

---

# Final judge checklist

Before presenting, complete and verify:

- [ ] Replace role labels with actual team member names.
- [ ] Publish the project to a public GitHub repository.
- [ ] Add an explicit open-source license file.
- [ ] Add the public repository URL to the website and README.
- [ ] Connect a live Gemma 4 endpoint or clearly label the model integration as the Hack Day target.
- [ ] Keep the deterministic fallback available for a reliable demo.
- [ ] Demonstrate baseline → protected → approval → replay → regression test.
- [ ] State clearly that the refund is synthetic and no real payment occurs.
- [ ] Show the onboarding video and README to mentors.
- [ ] Prepare a 30-second pitch and a 3-minute technical walkthrough.

## Closing statement

MemoryFirewall makes AI-agent memory behave more like a controlled software dependency: provenance is visible, high-impact use is enforced, decisions are explainable, and failures become tests. Gemma adds open-weight reasoning where language understanding is valuable, while deterministic policy protects the final action boundary.
