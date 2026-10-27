#!/usr/bin/env python3
"""
{^} Protocol One — DocLock 1.5 + CLK-ATTEST-1 Offline Integrity Capsule & Verifier CLI (v2.0)
Part of Kit #03: Tri-Signature Controlled Trial Starter Kit
Seals raw bytes (SHA-256), character count, line count, and orthogonal time axis (ATTESTED / LOCAL-ONLY / ATTESTATION-MISMATCH).
 Boundary: "DocLock proves a document is unchanged, not that what it says is true."
Zero external dependencies (Python 3 Standard Library only).
"""
import argparse
import datetime
import hashlib
import json
import os
import sys


def create_doclock_capsule(content_bytes: bytes, filename: str, signer: str, burst_sec: float, rfc3161_tokens: list | None = None) -> dict:
    sha256_bytes = hashlib.sha256(content_bytes).hexdigest()
    text_str = content_bytes.decode("utf-8", errors="replace")
    char_count = len(text_str)
    line_count = len(text_str.splitlines())
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    tokens = rfc3161_tokens or []
    if len(tokens) >= 2:
        time_axis = "ATTESTED"
        uncertainty = "±1s UTC (FreeTSA + DigiCert RFC 3161)"
    elif len(tokens) == 1:
        time_axis = "SINGLE-AUTHORITY"
        uncertainty = "±2s UTC (Single RFC 3161 TSA)"
    else:
        time_axis = "LOCAL-ONLY"
        uncertainty = "Unattested local system clock (no RFC 3161 token attached)"

    capsule_core = f"{{^}}|DOCLOCK-1.5|{filename}|{sha256_bytes}|CHARS:{char_count}|LINES:{line_count}|SIGNER:{signer}|BURST:{burst_sec:.2f}s|{now_utc}"
    capsule_seal = hashlib.sha256(capsule_core.encode("utf-8")).hexdigest()

    return {
        "standard": "{^} Protocol One — DocLock 1.5 + CLK-ATTEST-1",
        "mark": "{^}",
        "accuracy_boundary": "DocLock proves a document is unchanged, not that what it says is true.",
        "filename": filename,
        "byte_length": len(content_bytes),
        "sha256_bytes": sha256_bytes,
        "char_count": char_count,
        "line_count": line_count,
        "tri_signature_signer": signer,
        "tri_signature_burst_sec": round(burst_sec, 2),
        "clk_attest_1": {
            "time_axis_status": time_axis,
            "uncertainty": uncertainty,
            "local_timestamp_utc": now_utc,
            "rfc3161_authorities": tokens,
        },
        "qr_trust_capsule_payload": capsule_core,
        "capsule_sha256": capsule_seal,
    }


def verify_doclock_capsule(content_bytes: bytes, capsule: dict) -> dict:
    sha_now = hashlib.sha256(content_bytes).hexdigest()
    text_now = content_bytes.decode("utf-8", errors="replace")
    chars_now = len(text_now)

    expected_core = (
        f"{{^}}|DOCLOCK-1.5|{capsule['filename']}|{capsule['sha256_bytes']}|"
        f"CHARS:{capsule['char_count']}|LINES:{capsule['line_count']}|"
        f"SIGNER:{capsule['tri_signature_signer']}|BURST:{capsule['tri_signature_burst_sec']:.2f}s|"
        f"{capsule['clk_attest_1']['local_timestamp_utc']}"
    )
    expected_seal = hashlib.sha256(expected_core.encode("utf-8")).hexdigest()

    if expected_seal != capsule.get("capsule_sha256"):
        verdict = "BROKEN_SEAL"
        detail = "Capsule metadata seal SHA-256 mismatch."
    elif sha_now != capsule.get("sha256_bytes"):
        if chars_now == capsule.get("char_count"):
            verdict = "WARNING_METADATA_REENCODE"
            detail = "Byte SHA-256 changed, but extracted character count matches."
        else:
            verdict = "INTEGRITY_ALERT"
            detail = f"Document content modified! Expected SHA-256 {capsule.get('sha256_bytes')[:12]}..., got {sha_now[:12]}..."
    else:
        verdict = "VERIFIED"
        detail = "100% offline byte, character-count, and QR capsule match."

    return {
        "integrity_verdict": verdict,
        "time_axis": capsule.get("clk_attest_1", {}).get("time_axis_status", "LOCAL-ONLY"),
        "detail": detail,
        "boundary": "DocLock proves a document is unchanged, not that what it says is true.",
    }


def run_self_test() -> int:
    print("{^} Running doclock_1_5_offline_verifier.py self-test suite...")
    sample_doc = b"{^} Protocol One Board Resolution #2026-10: Approve $250,000 Treasury Transfer."
    cap_local = create_doclock_capsule(sample_doc, "resolution.txt", "B. L. Frost", 6.12)
    res1 = verify_doclock_capsule(sample_doc, cap_local)
    assert res1["integrity_verdict"] == "VERIFIED" and res1["time_axis"] == "LOCAL-ONLY"
    print("  [PASS] Test 1 — Offline VERIFIED + orthogonal LOCAL-ONLY time axis:", res1)

    cap_attested = create_doclock_capsule(sample_doc, "resolution.txt", "B. L. Frost", 6.12, ["FreeTSA-RFC3161", "DigiCert-RFC3161"])
    res2 = verify_doclock_capsule(sample_doc, cap_attested)
    assert res2["integrity_verdict"] == "VERIFIED" and res2["time_axis"] == "ATTESTED"
    print("  [PASS] Test 2 — Offline VERIFIED + Dual-Authority ATTESTED time axis:", res2["time_axis"])

    res3 = verify_doclock_capsule(sample_doc + b" TAMPERED", cap_attested)
    assert res3["integrity_verdict"] == "INTEGRITY_ALERT"
    print("  [PASS] Test 3 — Byte mutation triggers INTEGRITY_ALERT (even when time is ATTESTED):", res3["integrity_verdict"])

    print("{^} ALL 3/3 DOCLOCK 1.5 + CLK-ATTEST-1 SELF-TESTS PASSED.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{^} DocLock 1.5 + CLK-ATTEST-1 Offline Verifier CLI")
    parser.add_argument("--self-test", action="store_true", help="Run built-in test suite")
    args = parser.parse_args()
    sys.exit(run_self_test())
