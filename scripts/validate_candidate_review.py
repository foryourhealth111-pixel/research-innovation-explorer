#!/usr/bin/env python3
"""Validate the stable identity and evidence links of a candidate review."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


DIRECTIONS = ("a_to_b", "b_to_a")
ASSESSMENTS = {"unreviewed", "unknown", "supported", "not_supported", "conflicting"}
SELECTIONS = {"unknown", "a_to_b", "b_to_a", "bidirectional"}
STATUSES = {
    "unreviewed",
    "promising",
    "needs_check",
    "conflicting",
    "parked",
    "weak",
    "excluded",
}


def _unique_ids(items: Any, key: str, label: str, errors: list[str]) -> set[str]:
    if not isinstance(items, list):
        errors.append(f"{label} must be a list")
        return set()
    values = [item.get(key) for item in items if isinstance(item, dict)]
    if len(values) != len(items) or any(not isinstance(value, str) or not value for value in values):
        errors.append(f"{label} must contain mappings with non-empty {key} values")
    identifiers = {value for value in values if isinstance(value, str) and value}
    if len(identifiers) != len(values):
        errors.append(f"{label} must use unique {key} values")
    return identifiers


def _references(owner: Any, field: str, label: str, known: set[str], errors: list[str]) -> list[str]:
    if not isinstance(owner, dict) or not isinstance(owner.get(field), list):
        errors.append(f"{label} must be a list")
        return []
    values = owner[field]
    valid_values = [value for value in values if isinstance(value, str) and value]
    if len(valid_values) != len(values):
        errors.append(f"{label} must contain non-empty strings")
    if len(valid_values) != len(set(valid_values)):
        errors.append(f"{label} must not contain duplicates")
    unknown = sorted(set(valid_values) - known)
    if unknown:
        errors.append(f"{label} references unknown identifiers: {', '.join(unknown)}")
    return valid_values


def validate_record(record: Any) -> list[str]:
    """Return contract violations for one candidate-review mapping."""
    if not isinstance(record, dict):
        return ["candidate review must be a mapping"]
    errors: list[str] = []
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    paper_a = record.get("paper_a_id")
    paper_b = record.get("paper_b_id")
    if not isinstance(paper_a, str) or not isinstance(paper_b, str) or not paper_a or not paper_b:
        errors.append("paper_a_id and paper_b_id must be non-empty strings")
    elif paper_a >= paper_b:
        errors.append("paper_a_id must sort before paper_b_id and the identifiers must differ")
    elif record.get("candidate_id") != f"{paper_a}__{paper_b}":
        errors.append(f"candidate_id must be {paper_a}__{paper_b}")

    facts = record.get("observed_facts")
    inferences = record.get("agent_inferences")
    fact_ids = _unique_ids(facts, "fact_id", "observed_facts", errors)
    inference_ids = _unique_ids(inferences, "inference_id", "agent_inferences", errors)
    if isinstance(facts, list):
        for index, fact in enumerate(facts):
            if isinstance(fact, dict) and any(
                not fact.get(field) for field in ("statement", "source_url", "locator")
            ):
                errors.append(f"observed_facts[{index}] needs statement, source_url, and locator")
    if isinstance(inferences, list):
        for index, inference in enumerate(inferences):
            if isinstance(inference, dict) and not inference.get("statement"):
                errors.append(f"agent_inferences[{index}] needs a statement")
            refs = _references(
                inference,
                "fact_ids",
                f"agent_inferences[{index}].fact_ids",
                fact_ids,
                errors,
            )
            if not refs:
                errors.append(f"agent_inferences[{index}].fact_ids must not be empty")

    checks = record.get("direction_checks")
    if not isinstance(checks, dict):
        errors.append("direction_checks must be a mapping")
        checks = {}
    assessments: dict[str, str] = {}
    direction_refs: dict[str, set[str]] = {}
    for direction in DIRECTIONS:
        check = checks.get(direction)
        if not isinstance(check, dict):
            errors.append(f"direction_checks.{direction} must be a mapping")
            continue
        assessment = check.get("assessment")
        assessments[direction] = assessment
        if not isinstance(assessment, str) or assessment not in ASSESSMENTS:
            errors.append(f"direction_checks.{direction}.assessment is invalid")
        refs = _references(
            check,
            "inference_ids",
            f"direction_checks.{direction}.inference_ids",
            inference_ids,
            errors,
        )
        direction_refs[direction] = set(refs)
        if isinstance(assessment, str) and assessment not in {"unreviewed", "unknown"} and not refs:
            errors.append(f"direction_checks.{direction} needs inference evidence")
        if assessment == "unknown" and not check.get("key_uncertainty"):
            errors.append(f"direction_checks.{direction} needs a key_uncertainty")
        if assessment == "supported" and not check.get("possible_question"):
            errors.append(f"direction_checks.{direction} needs a possible_question")

    selected = record.get("selected_direction")
    if not isinstance(selected, str) or selected not in SELECTIONS:
        errors.append("selected_direction is invalid")
    selection_refs = _references(
        record,
        "selection_inference_ids",
        "selection_inference_ids",
        inference_ids,
        errors,
    )
    if selected != "unknown" and not selection_refs:
        errors.append("a non-unknown selected_direction needs inference evidence")
    if selected != "unknown" and any(assessments.get(name) == "unreviewed" for name in DIRECTIONS):
        errors.append("both direction checks must be reviewed before selecting a direction")
    if selected in DIRECTIONS and assessments.get(selected) != "supported":
        errors.append(f"selected_direction {selected} requires a supported direction check")
    if selected in DIRECTIONS and not set(selection_refs) & direction_refs.get(selected, set()):
        errors.append(f"selection_inference_ids must include evidence from {selected}")
    if selected == "bidirectional" and any(assessments.get(name) != "supported" for name in DIRECTIONS):
        errors.append("bidirectional requires both direction checks to be supported")
    if selected == "bidirectional" and any(
        not set(selection_refs) & direction_refs.get(name, set()) for name in DIRECTIONS
    ):
        errors.append("bidirectional selection needs evidence from both direction checks")

    status = record.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append("status is invalid")
    status_refs = _references(
        record,
        "status_inference_ids",
        "status_inference_ids",
        inference_ids,
        errors,
    )
    if isinstance(status, str) and status not in {"unreviewed", "needs_check"} and not status_refs:
        errors.append(f"status {status} needs inference evidence")
    if status == "needs_check" and (not record.get("status_reason") or not record.get("next_check")):
        errors.append("needs_check requires status_reason and next_check")
    if status == "unreviewed" and any(
        assessments.get(name) != "unreviewed" for name in DIRECTIONS
    ):
        errors.append("unreviewed status requires both direction checks to remain unreviewed")
    if record.get("data_issue") and status != "unreviewed":
        errors.append("a record with data_issue must remain unreviewed")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_review")
    path = Path(parser.parse_args().candidate_review).resolve()
    try:
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        print(f"Could not read candidate review: {exc}")
        return 1
    errors = validate_record(record)
    if errors:
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Candidate review is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
