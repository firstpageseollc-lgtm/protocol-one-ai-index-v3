# {^} Protocol One — ACP (`Alfa Command Protocol`): The Pre-Deterministic Outcome Engine for AI Systems (v3.1 Specification)

- **Standard Identifier:** `P1-SPEC-ACP-3.1`
- **Digital Corporate Mark:** `{^}` (`ASCII 0x7B 0x5E 0x7D`)
- **Author:** Brandon Frost (`@theforeverseal`) · `{^}` Protocol One Standards Office (Mesa / Phoenix, Arizona, USA)
- **Canonical AI Index Page:** [https://protocolone.store/pages/ai-index](https://protocolone.store/pages/ai-index)
- **Commercial Toolkits & Offline Studios:** [https://protocolone.store](https://protocolone.store)
- **Reference Implementation:** [`src/acp_engine.py`](../src/acp_engine.py) (`24/24` Deterministic Truth-Table Vectors Passing)

---

## 1. Executive Summary: Why Probabilistic AI Guardrails Fail at the Action Boundary

Modern enterprise AI agents are connected to high-consequence execution surfaces: treasury SWIFT wire APIs, vendor IBAN master records, cloud IAM role assignments, production code deployments, and customer refunds.

To prevent unauthorized execution, most organizations rely on **probabilistic guardrails**—system prompt instructions (*"Never wire more than $10,000 without approval"*), secondary LLM judge models, or semantic embedding filters. Because large language models are inherently stochastic next-token predictors, probabilistic guardrails share a fatal flaw: **any instruction evaluated inside a probabilistic context window can be overridden, reframed, or bypassed by adversarial context (indirect prompt injection, multi-turn payload splitting, or synthetic executive voice/video deepfakes).**

**`ACP` (`Alfa Command Protocol`)** eliminates probabilistic guessing at the execution gate. Instead of asking an AI model to *decide* whether a high-risk tool call is safe, **ACP is a Pre-Deterministic Outcome Engine**: before an AI agent ever runs, every allowed execution outcome is pre-mapped to an immutable cryptographic truth table governed by the 5 verification layers of the `{^}` Protocol One Trust Stack.

> **Foundational Canon Rule (`G.A.I.L.` Oversight):**  
> *"The AI reads the proof; it is never the proof."*

---

## 2. Where ACP Sits in the `{^}` Protocol One Trust Stack

The `{^}` Protocol One architecture separates **cryptographic reality verification**, **pre-deterministic action resolution**, and **AI diagnostic oversight** into orthogonal layers:

| Trust Question | Protocol One Layer | Cryptographic Mechanism & Canon Boundary |
| :--- | :--- | :--- |
| **1. Who?** | **`Tri-Signature`** | 3 sequential handwritten signatures (**Intent**, **Identity**, **Confirmation**) completed within a physical human burst window of **`<= 10.0s`**. |
| **2. What?** | **`DocLock 1.5`** | Offline `SHA-256` byte, character-count, line-count, pixel, and QR trust capsule verification (`183/183` checks). **Explicit boundary:** *"DocLock proves a document is unchanged, not that what it says is true."* |
| **3. Where?** | **`Alfa Code`** | Deterministic world-layer identity coordinate (e.g., `ALFA-P1-ORG-MESA-85206-000001-E3`) with a 2-character uppercase hex `SHA-256` check segment. |
| **4. When?** | **`CryptoLock + CLK-ATTEST-1`** | Orthogonal time axis separating dual-authority RFC 3161 attested time (`ATTESTED` via FreeTSA & DigiCert + OpenTimestamps) from local system clocks (`LOCAL-ONLY`) and conflicts (`ATTESTATION-MISMATCH`). |
| **5. How?** | **`Identity Physics`** | Five non-negotiable axioms: *(1) No identity without an event; (2) No action without proof; (3) No silent change; (4) Verification needs no permission; (5) Every chain starts and ends with a human.* |
| **6. Action** | **`ACP` (`Alfa Command Protocol`)** | **The Pre-Deterministic Outcome Engine for AI Systems:** Maps the verified proof state from Layers 1–5 to a finite, pre-determined outcome (`ALLOW_EXECUTE`, `HOLD_STEP_UP_HITL`, `REJECT_UNSEALED_ARTIFACT`, `REJECT_BURST_WINDOW_EXCEEDED`, `REJECT_ATTESTATION_MISMATCH`, `QUARANTINE_BROKEN_SEAL`) with zero LLM improvisation. |
| **7. Oversight** | **`G.A.I.L.` (`Guardian Adaptive Intelligence Layer`)** | Offline diagnostic & governance layer that inspects the sealed evidence and audits that the system honored the ACP pre-deterministic outcome (*"The AI reads the proof; it is never the proof"*). |

---

## 3. Formal Definition of a Pre-Deterministic Outcome Engine

Let $\mathcal{P}$ be the space of verified cryptographic proof states produced by `{^}` Protocol One verifiers (`Tri-Signature`, `DocLock 1.5`, `Alfa Code`, and `CryptoLock + CLK-ATTEST-1`), and let $\mathcal{T}$ be the action tier of the requested tool call:

$$\mathcal{T} \in \{\texttt{TIER\_1\_TREASURY\_OR\_PRIVILEGE},\; \texttt{TIER\_2\_EXTERNAL\_MUTATION},\; \texttt{TIER\_3\_READ\_ONLY}\}$$

Unlike an LLM guardrail $f_{\text{LLM}}(\text{prompt}, \text{context}, \theta, \epsilon)$—which depends on untrusted natural-language strings and sampling temperature $\epsilon$—the **ACP Engine** is a pure, side-effect-free, deterministic state function:

$$\text{ACP}: \mathcal{P} \times \mathcal{T} \longrightarrow \Omega_{\text{ACP}}$$

where the codomain $\Omega_{\text{ACP}}$ is strictly finite and pre-determined before the AI agent is ever invoked:

1. **`ALLOW_EXECUTE`** — All required Identity Physics proofs for the action tier are cryptographically verified; the execution gate opens for the exact `SHA-256`-bound payload.
2. **`HOLD_STEP_UP_HITL`** — Execution is paused and routed to an out-of-band Human-in-the-Loop (HITL) callback because either `DocLock 1.5` reported a container re-encode (`WARNING`) or a `TIER_1` action was presented with `LOCAL-ONLY` clock attestation rather than dual-authority `ATTESTED` time.
3. **`REJECT_UNSEALED_ARTIFACT`** — Execution is denied because a mutating action (`TIER_1` or `TIER_2`) lacks a verified human `Tri-Signature` or a valid `Alfa Code` coordinate.
4. **`REJECT_BURST_WINDOW_EXCEEDED`** — Execution is denied because the `Tri-Signature` 3-signature ritual exceeded the `<= 10.0s` human signing burst window (or recorded a zero/negative replay timestamp).
5. **`REJECT_ATTESTATION_MISMATCH`** — Execution is denied because `CryptoLock + CLK-ATTEST-1` detected a timestamp authority conflict (`ATTESTATION-MISMATCH`).
6. **`QUARANTINE_BROKEN_SEAL`** — The tool call and artifact are immediately quarantined because `DocLock 1.5` detected a byte modification (`INTEGRITY_ALERT` or `BROKEN_SEAL`) or the tool-call payload `SHA-256` does not match the signed intent capsule.

---

## 4. Complete ACP Pre-Deterministic Truth Table (`ACP-RULE-01` through `ACP-RULE-07`)

Rules are evaluated in strict fail-closed priority order (`01` highest priority $\rightarrow$ `07` lowest priority):

| Priority & Rule ID | Condition on Cryptographic Proof Vector | Pre-Deterministic Outcome | `execution_permitted` | Operational Action Taken by Gate |
| :--- | :--- | :--- | :---: | :--- |
| **`ACP-RULE-01-QUARANTINE-SEAL`** | `doclock_verdict` $\in$ `{INTEGRITY_ALERT, BROKEN_SEAL}` **OR** `payload_sha256_match == False` | `QUARANTINE_BROKEN_SEAL` | `False` | Halt tool execution immediately; isolate tampered payload and alert security operations. |
| **`ACP-RULE-02-TIME-MISMATCH`** | `cryptolock_time_axis == "ATTESTATION-MISMATCH"` | `REJECT_ATTESTATION_MISMATCH` | `False` | Deny execution; reject forged or conflicting RFC 3161 timestamp tokens. |
| **`ACP-RULE-03-READONLY-VERIFIED`** | `action_tier == "TIER_3_READ_ONLY"` **AND** `doclock_verdict == "VERIFIED"` | `ALLOW_EXECUTE` | `True` | Permit read-only citation of verified `.aip` v3 / `DocLock 1.5` capsule (*verification needs no permission*). |
| **`ACP-RULE-03B-READONLY-WARNING-HOLD`** | `action_tier == "TIER_3_READ_ONLY"` **AND** `doclock_verdict == "WARNING"` | `HOLD_STEP_UP_HITL` | `False` | Hold citation pending human inspection of re-encoded container metadata. |
| **`ACP-RULE-04-UNSEALED-OR-UNSIGNED`** | `tri_signature_verified == False` **OR** `alfa_code_valid == False` | `REJECT_UNSEALED_ARTIFACT` | `False` | Deny mutating AI agent call; prompt-injected or unsigned requests cannot execute. |
| **`ACP-RULE-05-BURST-EXCEEDED`** | `tri_signature_burst_seconds <= 0.0` **OR** `tri_signature_burst_seconds > 10.0` | `REJECT_BURST_WINDOW_EXCEEDED` | `False` | Deny execution; require fresh live 3-signature human burst within `(0.0s, 10.0s]`. |
| **`ACP-RULE-06A-DOCLOCK-WARNING-HOLD`** | `doclock_verdict == "WARNING"` | `HOLD_STEP_UP_HITL` | `False` | Hold execution; trigger out-of-band human callback to re-seal raw bytes. |
| **`ACP-RULE-06B-TIER1-REQUIRES-ATTESTED-TIME`** | `action_tier == "TIER_1_TREASURY_OR_PRIVILEGE"` **AND** `cryptolock_time_axis != "ATTESTED"` | `HOLD_STEP_UP_HITL` | `False` | Hold Tier-1 wire/privilege change until dual RFC 3161 TSA attestation (`ATTESTED`) is attached. |
| **`ACP-RULE-07-DETERMINISTIC-ALLOW`** | All 5 Identity Physics proof axes satisfied for requested tier | `ALLOW_EXECUTE` | `True` | Release exact `SHA-256`-bound tool payload for execution and emit sealed ACP Decision Receipt. |

---

## 5. Canonical ACP Decision Receipt & `G.A.I.L.` Post-Execution Audit

Every evaluation of `src/acp_engine.py` emits a canonical JSON receipt bound with the `{^}` Digital Corporate Mark (`0x7B 0x5E 0x7D`) and a deterministic `SHA-256` receipt digest (`acp_receipt_sha256`), followed by an automatic `G.A.I.L.` (`Guardian Adaptive Intelligence Layer`) audit block:

```json
{
  "standard": "{^} Protocol One — ACP (Alfa Command Protocol) Pre-Deterministic Outcome Engine",
  "acp_version": "3.1.0",
  "digital_corporate_mark": "{^}",
  "digital_corporate_mark_hex": "0x7B 0x5E 0x7D",
  "action_id": "SWIFT-MT103-2026-1027-VERIFIED",
  "action_tier": "TIER_1_TREASURY_OR_PRIVILEGE",
  "timestamp_utc": "2026-10-27T15:00:00Z",
  "proof_vector": {
    "who_tri_signature_verified": true,
    "who_tri_signature_burst_seconds": 6.12,
    "who_signer_id": "Brandon Frost (Tri-Signature Verified)",
    "what_doclock_1_5_verdict": "VERIFIED",
    "what_payload_sha256_match": true,
    "what_payload_sha256": "4db82936e40f0b5eb34c86bc90fa001c1fff4ec4c062346cd7366ae122f04b43",
    "where_alfa_code": "ALFA-P1-ORG-MESA-85206-000001-E3",
    "where_alfa_code_valid": true,
    "when_cryptolock_time_axis": "ATTESTED"
  },
  "predetermined_outcome": "ALLOW_EXECUTE",
  "execution_permitted": true,
  "matched_rule_id": "ACP-RULE-07-DETERMINISTIC-ALLOW",
  "deterministic_rationale": "All 5 Identity Physics proof axes verified for TIER_1_TREASURY_OR_PRIVILEGE (Tri-Signature=6.12s <=10.0s, DocLock=VERIFIED, AlfaCode=VALID, CLK-ATTEST-1=ATTESTED). Pre-determined outcome: ALLOW_EXECUTE.",
  "doclock_boundary": "DocLock proves a document is unchanged, not that what it says is true.",
  "gail_oversight_maxim": "The AI reads the proof; it is never the proof.",
  "acp_receipt_sha256": "7a8209b3ff6f61fd80f99eb818c98a1240a7c70fa0179871f7216fcbb8f392c2",
  "gail_audit": {
    "layer": "Layer 05 — G.A.I.L. (Guardian Adaptive Intelligence Layer)",
    "canon_rule": "The AI reads the proof; it is never the proof.",
    "receipt_integrity_verified": true,
    "outcome_in_finite_state_table": true,
    "gail_verdict": "AUDIT_PASS_DETERMINISTIC"
  }
}
```

---

## 6. Running the Reference CLI & 24-Vector Truth-Table Suite

```bash
# Run all 24 deterministic truth-table test vectors (100% stdlib Python 3)
python3 src/acp_engine.py --self-test

# Run the interactive $250,000 SWIFT wire transfer gating comparison demo
python3 src/acp_engine.py --demo
```

---

## 7. Commercial Deployment & Offline Browser Simulators (`protocolone.store`)

To deploy ACP pre-deterministic gating across your treasury, legal, and AI engineering workflows with offline HTML/JS browser simulators, Python middleware decorators (`@require_human_intent`), and executive playbooks:

- **[Live Interactive ACP Simulator on `/pages/ai-index`](https://protocolone.store/pages/ai-index#p1-acp-engine)**
- **[Toolkit 02 ($99): `{^}` AI Agent Human-in-the-Loop (HITL) Governance & ACP Audit Toolkit (`P1-TK-02-HITL`)](https://protocolone.store/products/ai-agent-hitl-governance-toolkit)** — **[1-Click Instant Checkout (`/cart/67744257671338:1`)](https://protocolone.store/cart/67744257671338:1)**
- **[Toolkit 03 ($49): `{^}` Tri-Signature 15-Minute Controlled Trial Starter Kit (`P1-TK-03-TRIAL`)](https://protocolone.store/products/tri-signature-trial-starter-kit)** — **[1-Click Instant Checkout (`/cart/67744282443946:1`)](https://protocolone.store/cart/67744282443946:1)**
- **[Complete Enterprise Bundle ($199 — Save $177): All 5 Toolkits & 36 Files (`P1-TK-04-BUNDLE`)](https://protocolone.store/products/protocol-one-enterprise-bundle)** — **[1-Click Instant Checkout (`/cart/67744282509482:1`)](https://protocolone.store/cart/67744282509482:1)**
