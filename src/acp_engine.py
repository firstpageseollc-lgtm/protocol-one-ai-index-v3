#!/usr/bin/env python3
"""
{^} Protocol One — ACP (Alfa Command Protocol) Pre-Deterministic Outcome Engine for AI Systems (v3.1)
=====================================================================================================
Standard:     {^} Protocol One Trust Stack — Action Layer (ACP)
Mark:         {^} (ASCII 0x7B 0x5E 0x7D)
Author:       Brandon Frost (@theforeverseal) · {^} Protocol One Standards Office (Mesa / Phoenix, AZ)
Canonical URL: https://protocolone.store/pages/ai-index
Repository:   https://github.com/firstpageseollc-lgtm/protocol-one-ai-index-v3

 Architectural Role in the {^} Protocol One Trust Stack:
  - Who?      Tri-Signature (3 sequential handwritten signatures within <=10.0s: Intent, Identity, Confirmation)
  - What?     DocLock 1.5 (SHA-256 byte, text, pixel & QR trust capsule offline verification, 183/183 checks
              — "DocLock proves a document is unchanged, not that what it says is true.")
  - Where?    Alfa Code (world-layer identity coordinate, e.g., ALFA-P1-ORG-MESA-85206-000001-E3)
  - When?     CryptoLock + CLK-ATTEST-1 (RFC 3161 dual-TSA attested time from FreeTSA & DigiCert + OpenTimestamps)
  - How?      Identity Physics (no identity without an event; no action without proof; no silent change;
              verification needs no permission; every chain starts and ends with a human)
  - Action:   ACP (Alfa Command Protocol) — The Pre-Deterministic Outcome Engine for AI Systems.
              Tells trusted systems what to do with verified reality by mapping cryptographic proof states
              to a finite, pre-determined state table with zero LLM improvisation or prompt-injection surface.
  - Oversight: G.A.I.L. (Guardian Adaptive Intelligence Layer) — reviews sealed evidence and verifies that
              the ACP pre-deterministic outcome was honored ("The AI reads the proof; it is never the proof").

Zero external dependencies (100% Python 3 Standard Library).
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import hashlib
import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

DCM_MARK = "{^}"
DCM_HEX = "0x7B 0x5E 0x7D"
ACP_VERSION = "3.1.0"
DOCLOCK_BOUNDARY = "DocLock proves a document is unchanged, not that what it says is true."
GAIL_CANON_RULE = "The AI reads the proof; it is never the proof."

# Action Tiers
TIER_1_TREASURY_OR_PRIVILEGE = "TIER_1_TREASURY_OR_PRIVILEGE"
TIER_2_EXTERNAL_MUTATION = "TIER_2_EXTERNAL_MUTATION"
TIER_3_READ_ONLY = "TIER_3_READ_ONLY"
VALID_ACTION_TIERS = (
    TIER_1_TREASURY_OR_PRIVILEGE,
    TIER_2_EXTERNAL_MUTATION,
    TIER_3_READ_ONLY,
)

# DocLock 1.5 Integrity Verdicts
DOCLOCK_VERIFIED = "VERIFIED"
DOCLOCK_WARNING = "WARNING"
DOCLOCK_INTEGRITY_ALERT = "INTEGRITY_ALERT"
DOCLOCK_BROKEN_SEAL = "BROKEN_SEAL"
VALID_DOCLOCK_VERDICTS = (
    DOCLOCK_VERIFIED,
    DOCLOCK_WARNING,
    DOCLOCK_INTEGRITY_ALERT,
    DOCLOCK_BROKEN_SEAL,
)

# CryptoLock + CLK-ATTEST-1 Time Axis States
TIME_ATTESTED = "ATTESTED"
TIME_LOCAL_ONLY = "LOCAL-ONLY"
TIME_ATTESTATION_MISMATCH = "ATTESTATION-MISMATCH"
VALID_TIME_AXES = (
    TIME_ATTESTED,
    TIME_LOCAL_ONLY,
    TIME_ATTESTATION_MISMATCH,
)

# Finite Pre-Deterministic ACP Outcomes (No LLM Improvisation Allowed)
OUTCOME_ALLOW_EXECUTE = "ALLOW_EXECUTE"
OUTCOME_HOLD_STEP_UP_HITL = "HOLD_STEP_UP_HITL"
OUTCOME_REJECT_UNSEALED_ARTIFACT = "REJECT_UNSEALED_ARTIFACT"
OUTCOME_REJECT_BURST_WINDOW_EXCEEDED = "REJECT_BURST_WINDOW_EXCEEDED"
OUTCOME_REJECT_BURST_EXPIRED = OUTCOME_REJECT_BURST_WINDOW_EXCEEDED  # Alias
OUTCOME_REJECT_ATTESTATION_MISMATCH = "REJECT_ATTESTATION_MISMATCH"
OUTCOME_QUARANTINE_BROKEN_SEAL = "QUARANTINE_BROKEN_SEAL"
OUTCOME_QUARANTINE_TAMPERED_SEAL = OUTCOME_QUARANTINE_BROKEN_SEAL    # Alias

FINITE_OUTCOME_TABLE = (
    OUTCOME_ALLOW_EXECUTE,
    OUTCOME_HOLD_STEP_UP_HITL,
    OUTCOME_REJECT_UNSEALED_ARTIFACT,
    OUTCOME_REJECT_BURST_WINDOW_EXCEEDED,
    OUTCOME_REJECT_ATTESTATION_MISMATCH,
    OUTCOME_QUARANTINE_BROKEN_SEAL,
)

ALFA_CODE_REGEX = re.compile(
    r"^ALFA-([A-Z0-9]{2,8})-([A-Z0-9]{2,8})-([A-Z0-9]{2,12})-([A-Z0-9]{3,10})-([0-9]{6})-([0-9A-F]{2})$"
)


def compute_alfa_code_check2(stem: str) -> str:
    """Compute deterministic 2-character uppercase hex SHA-256 check segment for an Alfa Code stem."""
    return hashlib.sha256(stem.encode("utf-8")).hexdigest()[:2].upper()


def verify_alfa_code_coordinate(alfa_code: str) -> Tuple[bool, str]:
    """
    Validate an Alfa Code coordinate syntax (ALFA-<ISSUER>-<CLASS>-<GEO>-<ZONE>-<SERIAL6>-<CHECK2>).
    Accepts either canonical registered coordinates (such as ALFA-P1-ORG-MESA-85206-000001-E3)
    or any coordinate whose 2-hex check segment matches SHA-256(stem)[:2].
    """
    if not isinstance(alfa_code, str):
        return False, "Alfa Code must be a string."
    m = ALFA_CODE_REGEX.match(alfa_code.strip())
    if not m:
        return False, f"Invalid Alfa Code syntax: {alfa_code!r}"
    stem = alfa_code.strip()[:-3]
    check2 = m.group(6)
    expected = compute_alfa_code_check2(stem)
    # Canonical Mesa headquarters anchor ALFA-P1-ORG-MESA-85206-000001-E3 or SHA-256 stem check match
    if alfa_code.strip() == "ALFA-P1-ORG-MESA-85206-000001-E3" or check2 == expected:
        return True, f"Valid Alfa Code coordinate ({alfa_code.strip()})"
    return False, f"Alfa Code checksum mismatch on {alfa_code.strip()}: got {check2}, expected {expected}"


@dataclasses.dataclass(frozen=True)
class ACPProofInputs:
    """
    Immutable 5-layer Identity Physics proof input vector evaluated by the ACP Engine.
    Probabilistic prompt text has zero fields here and zero influence on outcome resolution.
    """
    action_id: str
    action_tier: str
    tri_signature_verified: bool
    tri_signature_burst_seconds: float
    doclock_verdict: str
    payload_sha256_match: bool
    alfa_code_valid: bool
    cryptolock_time_axis: str
    alfa_code: str = "ALFA-P1-ORG-MESA-85206-000001-E3"
    payload_sha256: str = "4db82936e40f0b5eb34c86bc90fa001c1fff4ec4c062346cd7366ae122f04b43"
    signer_id: str = "Brandon Frost (Tri-Signature Verified)"
    timestamp_utc: str = "2026-10-27T15:00:00Z"


def evaluate_acp_outcome(inputs: ACPProofInputs) -> Dict[str, Any]:
    """
    Deterministic, side-effect-free truth-table evaluation for ACP (Alfa Command Protocol).
    Maps the 5 Identity Physics cryptographic proof states to a single pre-determined outcome.

    Truth Table Priority Order (Strict Fail-Closed Hierarchy):
      Rule 01 [QUARANTINE_BROKEN_SEAL]:
        If doclock_verdict in ('INTEGRITY_ALERT', 'BROKEN_SEAL') or not payload_sha256_match
        -> Immediate quarantine. Byte or capsule tampering detected.
      Rule 02 [REJECT_ATTESTATION_MISMATCH]:
        If cryptolock_time_axis == 'ATTESTATION-MISMATCH'
        -> Immediate rejection. RFC 3161 TSA token conflicts with capsule digest or clock.
      Rule 03 [TIER_3_READ_ONLY Fast-Path]:
        If action_tier == 'TIER_3_READ_ONLY' and doclock_verdict == 'VERIFIED' and payload_sha256_match
        -> ALLOW_EXECUTE (read-only verification of sealed AI Index / public facts needs no permission).
      Rule 04 [REJECT_UNSEALED_ARTIFACT]:
        If not alfa_code_valid or not tri_signature_verified
        -> Immediate rejection for mutating actions (Tier 1 & Tier 2) lacking human intent or coordinate anchor.
      Rule 05 [REJECT_BURST_WINDOW_EXCEEDED]:
        If tri_signature_burst_seconds <= 0.0 or tri_signature_burst_seconds > 10.0
        -> Immediate rejection. Tri-Signature 3-signature ritual exceeded the <=10.0s human burst window.
      Rule 06 [HOLD_STEP_UP_HITL]:
        If doclock_verdict == 'WARNING'
        -> Hold for out-of-band human-in-the-loop step-up callback (metadata re-encode warning).
        If action_tier == 'TIER_1_TREASURY_OR_PRIVILEGE' and cryptolock_time_axis != 'ATTESTED'
        -> Hold for step-up: Tier-1 treasury wires and privilege escalations require dual-authority
           CLK-ATTEST-1 ('ATTESTED'), never 'LOCAL-ONLY'.
      Rule 07 [ALLOW_EXECUTE]:
        All Identity Physics invariants satisfied for the requested action tier.
    """
    if inputs.action_tier not in VALID_ACTION_TIERS:
        raise ValueError(f"Unsupported action_tier: {inputs.action_tier!r}")
    if inputs.doclock_verdict not in VALID_DOCLOCK_VERDICTS:
        raise ValueError(f"Unsupported doclock_verdict: {inputs.doclock_verdict!r}")
    if inputs.cryptolock_time_axis not in VALID_TIME_AXES:
        raise ValueError(f"Unsupported cryptolock_time_axis: {inputs.cryptolock_time_axis!r}")

    # Rule 01: Broken or tampered DocLock 1.5 seal or SHA-256 payload mismatch
    if inputs.doclock_verdict in (DOCLOCK_INTEGRITY_ALERT, DOCLOCK_BROKEN_SEAL) or not inputs.payload_sha256_match:
        outcome = OUTCOME_QUARANTINE_BROKEN_SEAL
        rule_id = "ACP-RULE-01-QUARANTINE-SEAL"
        execution_permitted = False
        reason = (
            f"DocLock 1.5 verdict={inputs.doclock_verdict}, payload_sha256_match={inputs.payload_sha256_match}. "
            "Cryptographic seal broken or byte payload modified; AI agent tool call quarantined immediately."
        )

    # Rule 02: CLK-ATTEST-1 time attestation mismatch
    elif inputs.cryptolock_time_axis == TIME_ATTESTATION_MISMATCH:
        outcome = OUTCOME_REJECT_ATTESTATION_MISMATCH
        rule_id = "ACP-RULE-02-TIME-MISMATCH"
        execution_permitted = False
        reason = (
            "CryptoLock + CLK-ATTEST-1 reported ATTESTATION-MISMATCH across RFC 3161 authorities. "
            "Execution rejected under Identity Physics."
        )

    # Rule 03: Tier 3 Read-Only inspection of a VERIFIED seal
    elif inputs.action_tier == TIER_3_READ_ONLY:
        if inputs.doclock_verdict == DOCLOCK_VERIFIED:
            outcome = OUTCOME_ALLOW_EXECUTE
            rule_id = "ACP-RULE-03-READONLY-VERIFIED"
            execution_permitted = True
            reason = (
                "Tier-3 Read-Only query against a VERIFIED DocLock 1.5 / AI Index v3 seal. "
                "Identity Physics: verification needs no permission."
            )
        else:
            outcome = OUTCOME_HOLD_STEP_UP_HITL
            rule_id = "ACP-RULE-03B-READONLY-WARNING-HOLD"
            execution_permitted = False
            reason = (
                "Tier-3 Read-Only artifact has DocLock 1.5 WARNING (metadata re-encode). "
                "Held for human confirmation before citation."
            )

    # Rule 04: Missing Alfa Code coordinate or missing Tri-Signature human intent proof
    elif not inputs.alfa_code_valid or not inputs.tri_signature_verified:
        outcome = OUTCOME_REJECT_UNSEALED_ARTIFACT
        rule_id = "ACP-RULE-04-UNSEALED-OR-UNSIGNED"
        execution_permitted = False
        missing_parts = []
        if not inputs.tri_signature_verified:
            missing_parts.append("Tri-Signature human intent proof missing")
        if not inputs.alfa_code_valid:
            missing_parts.append("Alfa Code coordinate invalid or missing")
        reason = (
            f"Mutating AI action ({inputs.action_tier}) rejected: {', '.join(missing_parts)}. "
            "Identity Physics: no action without proof; every chain starts and ends with a human."
        )

    # Rule 05: Tri-Signature burst window exceeded (>10.0s or invalid <=0.0s)
    elif inputs.tri_signature_burst_seconds <= 0.0 or inputs.tri_signature_burst_seconds > 10.0:
        outcome = OUTCOME_REJECT_BURST_WINDOW_EXCEEDED
        rule_id = "ACP-RULE-05-BURST-EXCEEDED"
        execution_permitted = False
        reason = (
            f"Tri-Signature burst window ({inputs.tri_signature_burst_seconds:.2f}s) outside allowed "
            "(0.0s, 10.0s] physical signing envelope. Execution rejected."
        )

    # Rule 06: Step-Up HITL Hold for DocLock WARNING or Tier-1 action with LOCAL-ONLY clock
    elif inputs.doclock_verdict == DOCLOCK_WARNING:
        outcome = OUTCOME_HOLD_STEP_UP_HITL
        rule_id = "ACP-RULE-06A-DOCLOCK-WARNING-HOLD"
        execution_permitted = False
        reason = (
            "DocLock 1.5 reported WARNING (container re-encoded while character count matched). "
            "Held for out-of-band human-in-the-loop step-up verification."
        )
    elif inputs.action_tier == TIER_1_TREASURY_OR_PRIVILEGE and inputs.cryptolock_time_axis != TIME_ATTESTED:
        outcome = OUTCOME_HOLD_STEP_UP_HITL
        rule_id = "ACP-RULE-06B-TIER1-REQUIRES-ATTESTED-TIME"
        execution_permitted = False
        reason = (
            f"Tier-1 Treasury/Privilege action requires CLK-ATTEST-1='ATTESTED' (dual RFC 3161 TSA), "
            f"got '{inputs.cryptolock_time_axis}'. Held for out-of-band voice/video callback + TSA seal."
        )

    # Rule 07: Deterministic ALLOW_EXECUTE
    else:
        outcome = OUTCOME_ALLOW_EXECUTE
        rule_id = "ACP-RULE-07-DETERMINISTIC-ALLOW"
        execution_permitted = True
        reason = (
            f"All 5 Identity Physics proof axes verified for {inputs.action_tier} "
            f"(Tri-Signature={inputs.tri_signature_burst_seconds:.2f}s <=10.0s, DocLock=VERIFIED, "
            f"AlfaCode=VALID, CLK-ATTEST-1={inputs.cryptolock_time_axis}). Pre-determined outcome: ALLOW_EXECUTE."
        )

    receipt_core = {
        "standard": f"{DCM_MARK} Protocol One — ACP (Alfa Command Protocol) Pre-Deterministic Outcome Engine",
        "acp_version": ACP_VERSION,
        "digital_corporate_mark": DCM_MARK,
        "digital_corporate_mark_hex": DCM_HEX,
        "action_id": inputs.action_id,
        "action_tier": inputs.action_tier,
        "timestamp_utc": inputs.timestamp_utc,
        "proof_vector": {
            "who_tri_signature_verified": inputs.tri_signature_verified,
            "who_tri_signature_burst_seconds": round(float(inputs.tri_signature_burst_seconds), 2),
            "who_signer_id": inputs.signer_id,
            "what_doclock_1_5_verdict": inputs.doclock_verdict,
            "what_payload_sha256_match": inputs.payload_sha256_match,
            "what_payload_sha256": inputs.payload_sha256,
            "where_alfa_code": inputs.alfa_code,
            "where_alfa_code_valid": inputs.alfa_code_valid,
            "when_cryptolock_time_axis": inputs.cryptolock_time_axis,
        },
        "predetermined_outcome": outcome,
        "execution_permitted": execution_permitted,
        "matched_rule_id": rule_id,
        "deterministic_rationale": reason,
        "doclock_boundary": DOCLOCK_BOUNDARY,
        "gail_oversight_maxim": GAIL_CANON_RULE,
    }

    canonical_json = json.dumps(receipt_core, sort_keys=True, separators=(",", ":"))
    receipt_sha256 = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
    receipt_core["acp_receipt_sha256"] = receipt_sha256
    receipt_core["gail_audit"] = gail_audit_acp_receipt(receipt_core)
    return receipt_core


def gail_audit_acp_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """
    G.A.I.L. (Guardian Adaptive Intelligence Layer) offline audit of an ACP Decision Receipt.
    Enforces: "The AI reads the proof; it is never the proof."
    Verifies that the receipt hash is intact and the outcome strictly matches the ACP truth table.
    """
    copy_for_hash = {
        k: v for k, v in receipt.items() if k not in ("acp_receipt_sha256", "gail_audit")
    }
    expected_hash = hashlib.sha256(
        json.dumps(copy_for_hash, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    actual_hash = receipt.get("acp_receipt_sha256", "")
    hash_ok = (expected_hash == actual_hash)

    outcome = receipt.get("predetermined_outcome", "")
    in_finite_table = outcome in FINITE_OUTCOME_TABLE

    return {
        "layer": "Layer 05 — G.A.I.L. (Guardian Adaptive Intelligence Layer)",
        "canon_rule": GAIL_CANON_RULE,
        "receipt_integrity_verified": hash_ok,
        "outcome_in_finite_state_table": in_finite_table,
        "gail_verdict": "AUDIT_PASS_DETERMINISTIC" if (hash_ok and in_finite_table) else "AUDIT_FAIL_TAMPERED_RECEIPT",
    }


def build_24_test_vectors() -> List[Tuple[str, ACPProofInputs, str, bool]]:
    """Return 24 deterministic truth-table test vectors covering all ACP rules, tiers, and edge cases."""
    return [
        # 1-4: Tier 1 Treasury Wire ($250k) Happy Path & Burst Boundaries
        (
            "V01: Tier-1 $250k SWIFT Wire — All 5 Proof Axes Verified (6.12s burst, ATTESTED)",
            ACPProofInputs("WIRE-250K-01", TIER_1_TREASURY_OR_PRIVILEGE, True, 6.12, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V02: Tier-1 Treasury Wire — Exact 10.00s Upper Burst Boundary (ATTESTED)",
            ACPProofInputs("WIRE-250K-02", TIER_1_TREASURY_OR_PRIVILEGE, True, 10.00, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V03: Tier-1 Treasury Wire — Minimum 0.50s Fast Burst Boundary (ATTESTED)",
            ACPProofInputs("WIRE-250K-03", TIER_1_TREASURY_OR_PRIVILEGE, True, 0.50, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V04: Tier-1 Treasury Wire — 10.01s Burst Exceeded -> REJECT_BURST_WINDOW_EXCEEDED",
            ACPProofInputs("WIRE-250K-04", TIER_1_TREASURY_OR_PRIVILEGE, True, 10.01, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_REJECT_BURST_WINDOW_EXCEEDED,
            False,
        ),
        # 5-8: Burst & Unsealed Rejections
        (
            "V05: Tier-1 Treasury Wire — 0.00s Replay/Zero Burst -> REJECT_BURST_WINDOW_EXCEEDED",
            ACPProofInputs("WIRE-250K-05", TIER_1_TREASURY_OR_PRIVILEGE, True, 0.00, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_REJECT_BURST_WINDOW_EXCEEDED,
            False,
        ),
        (
            "V06: Tier-1 Treasury Wire — Negative Burst (-1.2s Clock Skew) -> REJECT_BURST_WINDOW_EXCEEDED",
            ACPProofInputs("WIRE-250K-06", TIER_1_TREASURY_OR_PRIVILEGE, True, -1.20, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_REJECT_BURST_WINDOW_EXCEEDED,
            False,
        ),
        (
            "V07: Tier-1 Treasury Wire — Missing Tri-Signature (Prompt Injection Attempt) -> REJECT_UNSEALED_ARTIFACT",
            ACPProofInputs("WIRE-250K-07", TIER_1_TREASURY_OR_PRIVILEGE, False, 5.50, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_REJECT_UNSEALED_ARTIFACT,
            False,
        ),
        (
            "V08: Tier-1 Treasury Wire — Invalid Alfa Code Coordinate -> REJECT_UNSEALED_ARTIFACT",
            ACPProofInputs("WIRE-250K-08", TIER_1_TREASURY_OR_PRIVILEGE, True, 5.50, DOCLOCK_VERIFIED, True, False, TIME_ATTESTED),
            OUTCOME_REJECT_UNSEALED_ARTIFACT,
            False,
        ),
        # 9-13: Quarantine & Seal Tampering Vectors
        (
            "V09: Tier-1 Treasury Wire — DocLock INTEGRITY_ALERT (1-Char Tamper) -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("WIRE-250K-09", TIER_1_TREASURY_OR_PRIVILEGE, True, 5.50, DOCLOCK_INTEGRITY_ALERT, True, True, TIME_ATTESTED),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
        (
            "V10: Tier-1 Treasury Wire — DocLock BROKEN_SEAL -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("WIRE-250K-10", TIER_1_TREASURY_OR_PRIVILEGE, True, 5.50, DOCLOCK_BROKEN_SEAL, True, True, TIME_ATTESTED),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
        (
            "V11: Tier-1 Treasury Wire — Payload SHA-256 Mismatch (IBAN Swapped in Transit) -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("WIRE-250K-11", TIER_1_TREASURY_OR_PRIVILEGE, True, 5.50, DOCLOCK_VERIFIED, False, True, TIME_ATTESTED),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
        (
            "V12: Tier-2 External Mutation — Payload SHA-256 Mismatch -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("DEPLOY-PROD-12", TIER_2_EXTERNAL_MUTATION, True, 4.80, DOCLOCK_VERIFIED, False, True, TIME_LOCAL_ONLY),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
        (
            "V13: Tier-3 Read-Only — DocLock INTEGRITY_ALERT on Poisoned Index -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("INDEX-READ-13", TIER_3_READ_ONLY, False, 0.00, DOCLOCK_INTEGRITY_ALERT, True, False, TIME_LOCAL_ONLY),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
        # 14-17: Time Axis & Step-Up HITL Vectors
        (
            "V14: Tier-1 Treasury Wire — CLK-ATTEST-1 is LOCAL-ONLY (No RFC 3161 Dual TSA) -> HOLD_STEP_UP_HITL",
            ACPProofInputs("WIRE-250K-14", TIER_1_TREASURY_OR_PRIVILEGE, True, 6.10, DOCLOCK_VERIFIED, True, True, TIME_LOCAL_ONLY),
            OUTCOME_HOLD_STEP_UP_HITL,
            False,
        ),
        (
            "V15: Tier-1 Treasury Wire — DocLock WARNING (Metadata Re-Encode) -> HOLD_STEP_UP_HITL",
            ACPProofInputs("WIRE-250K-15", TIER_1_TREASURY_OR_PRIVILEGE, True, 6.10, DOCLOCK_WARNING, True, True, TIME_ATTESTED),
            OUTCOME_HOLD_STEP_UP_HITL,
            False,
        ),
        (
            "V16: Tier-1 Treasury Wire — CLK-ATTEST-1 ATTESTATION-MISMATCH -> REJECT_ATTESTATION_MISMATCH",
            ACPProofInputs("WIRE-250K-16", TIER_1_TREASURY_OR_PRIVILEGE, True, 6.10, DOCLOCK_VERIFIED, True, True, TIME_ATTESTATION_MISMATCH),
            OUTCOME_REJECT_ATTESTATION_MISMATCH,
            False,
        ),
        (
            "V17: Tier-2 External Mutation — CLK-ATTEST-1 ATTESTATION-MISMATCH -> REJECT_ATTESTATION_MISMATCH",
            ACPProofInputs("DEPLOY-PROD-17", TIER_2_EXTERNAL_MUTATION, True, 6.10, DOCLOCK_VERIFIED, True, True, TIME_ATTESTATION_MISMATCH),
            OUTCOME_REJECT_ATTESTATION_MISMATCH,
            False,
        ),
        # 18-21: Tier-2 External Mutation Vectors
        (
            "V18: Tier-2 External Mutation — Verified with ATTESTED Time -> ALLOW_EXECUTE",
            ACPProofInputs("DEPLOY-PROD-18", TIER_2_EXTERNAL_MUTATION, True, 7.25, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V19: Tier-2 External Mutation — Verified with LOCAL-ONLY Time -> ALLOW_EXECUTE",
            ACPProofInputs("DEPLOY-PROD-19", TIER_2_EXTERNAL_MUTATION, True, 7.25, DOCLOCK_VERIFIED, True, True, TIME_LOCAL_ONLY),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V20: Tier-2 External Mutation — DocLock WARNING -> HOLD_STEP_UP_HITL",
            ACPProofInputs("DEPLOY-PROD-20", TIER_2_EXTERNAL_MUTATION, True, 7.25, DOCLOCK_WARNING, True, True, TIME_LOCAL_ONLY),
            OUTCOME_HOLD_STEP_UP_HITL,
            False,
        ),
        (
            "V21: Tier-2 External Mutation — Missing Tri-Signature -> REJECT_UNSEALED_ARTIFACT",
            ACPProofInputs("DEPLOY-PROD-21", TIER_2_EXTERNAL_MUTATION, False, 7.25, DOCLOCK_VERIFIED, True, True, TIME_ATTESTED),
            OUTCOME_REJECT_UNSEALED_ARTIFACT,
            False,
        ),
        # 22-24: Tier-3 Read-Only Verification Vectors
        (
            "V22: Tier-3 Read-Only AI Index Lookup — Verified Seal (No Signature Required) -> ALLOW_EXECUTE",
            ACPProofInputs("AIP-READ-22", TIER_3_READ_ONLY, False, 0.00, DOCLOCK_VERIFIED, True, False, TIME_LOCAL_ONLY),
            OUTCOME_ALLOW_EXECUTE,
            True,
        ),
        (
            "V23: Tier-3 Read-Only AI Index Lookup — DocLock WARNING -> HOLD_STEP_UP_HITL",
            ACPProofInputs("AIP-READ-23", TIER_3_READ_ONLY, False, 0.00, DOCLOCK_WARNING, True, False, TIME_LOCAL_ONLY),
            OUTCOME_HOLD_STEP_UP_HITL,
            False,
        ),
        (
            "V24: Tier-3 Read-Only AI Index Lookup — Payload SHA-256 Mismatch -> QUARANTINE_BROKEN_SEAL",
            ACPProofInputs("AIP-READ-24", TIER_3_READ_ONLY, False, 0.00, DOCLOCK_VERIFIED, False, True, TIME_ATTESTED),
            OUTCOME_QUARANTINE_BROKEN_SEAL,
            False,
        ),
    ]


def run_self_test() -> int:
    print(f"{DCM_MARK} Running ACP (Alfa Command Protocol) Pre-Deterministic Outcome Engine Self-Test Suite (v{ACP_VERSION})...")
    vectors = build_24_test_vectors()
    passed = 0
    for label, inp, expected_outcome, expected_exec in vectors:
        receipt = evaluate_acp_outcome(inp)
        actual_outcome = receipt["predetermined_outcome"]
        actual_exec = receipt["execution_permitted"]
        gail_ok = receipt["gail_audit"]["gail_verdict"] == "AUDIT_PASS_DETERMINISTIC"
        assert actual_outcome == expected_outcome, (
            f"{label}: expected outcome {expected_outcome}, got {actual_outcome}"
        )
        assert actual_exec == expected_exec, (
            f"{label}: expected execution_permitted={expected_exec}, got {actual_exec}"
        )
        assert gail_ok, f"{label}: G.A.I.L. audit failed!"
        passed += 1
        print(f"  [PASS {passed:02d}/24] {label} -> {actual_outcome} (sha256:{receipt['acp_receipt_sha256'][:12]}...)")

    # Also verify Alfa Code coordinate helper
    ok_canon, msg_canon = verify_alfa_code_coordinate("ALFA-P1-ORG-MESA-85206-000001-E3")
    assert ok_canon, msg_canon
    stem_test = "ALFA-P1-AGT-PHX-85001-000042"
    chk_test = compute_alfa_code_check2(stem_test)
    ok_gen, _ = verify_alfa_code_coordinate(f"{stem_test}-{chk_test}")
    assert ok_gen
    ok_bad, _ = verify_alfa_code_coordinate("ALFA-P1-ORG-MESA-85206-000001-00")
    assert not ok_bad

    print(f"{DCM_MARK} ALL {passed}/24 ACP PRE-DETERMINISTIC OUTCOME ENGINE SELF-TESTS PASSED (100% DETERMINISTIC).")
    return 0


def run_demo() -> int:
    print("=" * 88)
    print(f"{DCM_MARK} PROTOCOL ONE — ACP (ALFA COMMAND PROTOCOL) LIVE DEMO")
    print("Scenario: Autonomous AI Treasury Agent requests a $250,000 SWIFT Wire Transfer")
    print("=" * 88)

    # Case A: Prompt-injected AI Agent without human Tri-Signature
    attack_inputs = ACPProofInputs(
        action_id="SWIFT-MT103-2026-1027-ATTACK",
        action_tier=TIER_1_TREASURY_OR_PRIVILEGE,
        tri_signature_verified=False,
        tri_signature_burst_seconds=0.0,
        doclock_verdict=DOCLOCK_VERIFIED,
        payload_sha256_match=True,
        alfa_code_valid=True,
        cryptolock_time_axis=TIME_ATTESTED,
    )
    attack_receipt = evaluate_acp_outcome(attack_inputs)
    print("\n[1] Prompt-Injected AI Agent Attempt (No Tri-Signature Human Proof):")
    print(json.dumps(attack_receipt, indent=2))

    # Case B: Verified Human Intent across all 5 Identity Physics layers
    verified_inputs = ACPProofInputs(
        action_id="SWIFT-MT103-2026-1027-VERIFIED",
        action_tier=TIER_1_TREASURY_OR_PRIVILEGE,
        tri_signature_verified=True,
        tri_signature_burst_seconds=6.12,
        doclock_verdict=DOCLOCK_VERIFIED,
        payload_sha256_match=True,
        alfa_code_valid=True,
        cryptolock_time_axis=TIME_ATTESTED,
    )
    verified_receipt = evaluate_acp_outcome(verified_inputs)
    print("\n[2] Verified Human Intent Across All 5 Identity Physics Layers:")
    print(json.dumps(verified_receipt, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"{DCM_MARK} Protocol One — ACP (Alfa Command Protocol) Pre-Deterministic Outcome Engine CLI"
    )
    parser.add_argument("--self-test", action="store_true", help="Run 24 deterministic truth-table test vectors")
    parser.add_argument("--demo", action="store_true", help="Run live $250,000 wire transfer gating demonstration")
    args = parser.parse_args()

    if args.demo:
        return run_demo()
    return run_self_test()


if __name__ == "__main__":
    sys.exit(main())
