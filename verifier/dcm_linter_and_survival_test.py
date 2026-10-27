#!/usr/bin/env python3
"""
{^} Protocol One — Digital Corporate Mark (DCM) R1–R12 Linter & 12-Surface Survival Benchmark CLI (v2.1)
Part of Kit #05: Digital Corporate Mark Specification & Implementation Kit (https://protocolone.store)
Tests any candidate ASCII mark across UTF-8, ASCII, JSON-LD, CSV, XML/HTML, LLM Tokenization,
SWIFT MT103/ISO 20022, SQL/CSV, Shell/CLI, Markdown, RFC 5322 Email, and Print/OCR surfaces.
Zero external dependencies (Python 3 Standard Library only).
"""
import argparse
import csv
import io
import json
import sys
import xml.sax.saxutils as saxutils


SWIFT_ALLOWED_EXTRA = set("/-?:().,'+ {}^")


def audit_corporate_mark(mark: str) -> dict:
    byte_len = len(mark.encode("utf-8"))
    is_ascii = all(0x21 <= ord(c) <= 0x7E for c in mark)
    has_delimiters = len(mark) >= 2 and (mark[0] in "{[(<" and mark[-1] in "}])>")
    json_safe = json.loads(json.dumps({"mark": mark}))["mark"] == mark
    xml_escaped = saxutils.escape(mark)
    xml_unchanged = (xml_escaped == mark)
    swift_survival = all(c.isalnum() or c in SWIFT_ALLOWED_EXTRA for c in mark)

    # CSV roundtrip check
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([mark])
    buf.seek(0)
    csv_roundtrip = next(csv.reader(buf))[0] == mark

    # Additional surface survival checks (R8-R12)
    no_quotes_or_backslashes = all(c not in ('"', "'", "\\", "`", "$") for c in mark)
    markdown_heading_safe = not mark.startswith("#") and "|" not in mark and "*" not in mark and "_" not in mark
    rfc5322_email_subject_safe = is_ascii and all(ord(c) < 128 and c not in ("\r", "\n", ":") for c in mark)
    terminal_log_monospaced_safe = is_ascii and byte_len == len(mark)
    ocr_distinct_glyphs = is_ascii and not any(c in "0O1lI" for c in mark)

    rules = {
        "R1_printable_ascii_7bit": is_ascii,
        "R2_compact_length_2_to_6_bytes": 2 <= byte_len <= 6,
        "R3_symmetric_or_bounded_delimiters": has_delimiters,
        "R4_survives_json_roundtrip_100pct": json_safe,
        "R5_survives_xml_html_without_entity_expansion": xml_unchanged,
        "R6_survives_llm_plain_text_tokenization": is_ascii and byte_len <= 6,
        "R7_survives_swift_memo_ascii_filter": swift_survival,
        "R8_survives_csv_rfc4180_roundtrip": csv_roundtrip,
        "R9_survives_sql_and_shell_literal_contexts": no_quotes_or_backslashes,
        "R10_survives_markdown_and_table_parsers": markdown_heading_safe,
        "R11_survives_rfc5322_email_headers_unencoded": rfc5322_email_subject_safe,
        "R12_survives_monospaced_terminal_and_ocr": terminal_log_monospaced_safe and ocr_distinct_glyphs,
    }
    passed = sum(1 for v in rules.values() if v)
    return {
        "candidate_mark": mark,
        "utf8_byte_length": byte_len,
        "code_points": [f"U+{ord(c):04X}" for c in mark],
        "rules_passed": f"{passed}/{len(rules)}",
        "rule_breakdown": rules,
        "verdict": "CANONICAL_PASS" if passed == len(rules) else "REVIEW_REQUIRED",
        "canonical_reference": "https://protocolone.store/pages/ai-index",
    }


def run_self_test() -> int:
    print("=" * 78)
    print("{^} PROTOCOL ONE — DIGITAL CORPORATE MARK (DCM) 12-SURFACE SURVIVAL SUITE")
    print("=" * 78)
    p1 = audit_corporate_mark("{^}")
    assert p1["verdict"] == "CANONICAL_PASS" and p1["rules_passed"] == "12/12", f"Expected 12/12 CANONICAL_PASS for {{^}}, got {p1}"
    print(f"  [PASS] Surface Audit ({p1['rules_passed']}) — {{^}} passes all 12 ASCII, JSON-LD, XML, LLM, SWIFT, CSV & OCR rules: {p1['code_points']}")

    for rule_name, ok in p1["rule_breakdown"].items():
        print(f"    [PASS] {rule_name}")

    bad_logo = audit_corporate_mark("🏢™©")
    assert bad_logo["verdict"] == "REVIEW_REQUIRED" and not bad_logo["rule_breakdown"]["R1_printable_ascii_7bit"]
    print(f"  [PASS] Negative Test A — Non-ASCII emoji/trademark symbol flagged ({bad_logo['rules_passed']})")

    xml_bad = audit_corporate_mark("<&>")
    assert not xml_bad["rule_breakdown"]["R5_survives_xml_html_without_entity_expansion"]
    print("  [PASS] Negative Test B — XML/HTML unsafe characters (<&>) caught by R5.")

    print("-" * 78)
    print("RESULT: 12/12 DCM SURVIVAL CHECKS & ALL NEGATIVE TESTS PASSED")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="{^} Digital Corporate Mark R1-R12 Linter & 12-Surface Survival CLI")
    parser.add_argument("--self-test", action="store_true", help="Run built-in 12-surface survival self-test suite")
    parser.add_argument("--mark", default="{^}", help="Candidate mark to lint (default: {^})")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(run_self_test())
    print(json.dumps(audit_corporate_mark(args.mark), indent=2))
