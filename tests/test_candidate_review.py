from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_idea_matrix import load_papers
from scripts.validate_candidate_review import validate_record


def valid_record() -> dict[str, object]:
    return {
        "schema_version": 1,
        "candidate_id": "A01__B03",
        "paper_a_id": "A01",
        "paper_b_id": "B03",
        "data_issue": None,
        "direction_checks": {
            "a_to_b": {
                "assessment": "supported",
                "possible_question": "Can mechanism A address limitation B?",
                "key_uncertainty": "Whether the settings are compatible",
                "inference_ids": ["I1"],
            },
            "b_to_a": {
                "assessment": "not_supported",
                "possible_question": "",
                "key_uncertainty": "",
                "inference_ids": ["I2"],
            },
        },
        "selected_direction": "a_to_b",
        "selection_inference_ids": ["I1"],
        "observed_facts": [
            {
                "fact_id": "F1",
                "statement": "Fact A",
                "source_url": "https://example.org/a",
                "locator": "Section 2",
            },
            {
                "fact_id": "F2",
                "statement": "Fact B",
                "source_url": "https://example.org/b",
                "locator": "Section 4",
            },
        ],
        "agent_inferences": [
            {"inference_id": "I1", "statement": "A may address B", "fact_ids": ["F1", "F2"]},
            {"inference_id": "I2", "statement": "The reverse lacks a role", "fact_ids": ["F1"]},
        ],
        "status": "promising",
        "status_reason": "I1 supports a bounded question.",
        "status_inference_ids": ["I1"],
        "next_check": "Compare evaluation settings",
    }


class CandidateReviewValidationTests(unittest.TestCase):
    def test_one_way_supported_record_is_valid(self) -> None:
        self.assertEqual(validate_record(valid_record()), [])

    def test_bidirectional_requires_evidence_for_both_directions(self) -> None:
        record = valid_record()
        record["selected_direction"] = "bidirectional"
        record["direction_checks"]["b_to_a"]["assessment"] = "supported"
        record["direction_checks"]["b_to_a"]["inference_ids"] = []
        errors = validate_record(record)
        self.assertTrue(any("b_to_a" in error and "evidence" in error for error in errors))

    def test_bidirectional_accepts_evidence_from_both_directions(self) -> None:
        record = valid_record()
        record["selected_direction"] = "bidirectional"
        record["selection_inference_ids"] = ["I1", "I2"]
        record["direction_checks"]["b_to_a"].update(
            assessment="supported",
            possible_question="Can mechanism B address limitation A?",
        )
        self.assertEqual(validate_record(record), [])

    def test_selection_requires_both_directions_to_be_reviewed(self) -> None:
        record = valid_record()
        record["direction_checks"]["b_to_a"]["assessment"] = "unreviewed"
        record["direction_checks"]["b_to_a"]["inference_ids"] = []
        errors = validate_record(record)
        self.assertIn("both direction checks must be reviewed before selecting a direction", errors)

    def test_reversed_candidate_identity_is_rejected(self) -> None:
        record = valid_record()
        record.update(candidate_id="B03__A01", paper_a_id="B03", paper_b_id="A01")
        errors = validate_record(record)
        self.assertTrue(any("paper_a_id must sort before" in error for error in errors))

    def test_unknown_inference_reference_is_rejected(self) -> None:
        record = valid_record()
        record["status_inference_ids"] = ["I404"]
        errors = validate_record(record)
        self.assertTrue(any("unknown identifiers: I404" in error for error in errors))

    def test_duplicate_paper_ids_fail_before_matrix_generation(self) -> None:
        fields = ["paper_id", "title", "task", "modules", "strengths", "weaknesses", "open_source"]
        row = {
            "paper_id": "A01",
            "title": "Paper",
            "task": "task",
            "modules": "module",
            "strengths": "strength",
            "weaknesses": "weakness",
            "open_source": "yes",
        }
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            path = Path(directory) / "papers.csv"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows([row, {**row, "title": "Duplicate"}])
            with self.assertRaisesRegex(ValueError, "Duplicate paper_id: A01"):
                load_papers(path)


if __name__ == "__main__":
    unittest.main()
