#!/usr/bin/env python3
"""Validate shared data, reports, dashboard, and optional Lark sync metadata."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from artifact_names import artifact_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--allow-missing-report", action="store_true")
    parser.add_argument("--allow-missing-html", action="store_true")
    args = parser.parse_args()
    root = args.output_dir.expanduser().resolve()
    errors: list[str] = []

    data_path = artifact_path(root, "analysis_data")
    csv_path = artifact_path(root, "article_features")
    if not data_path.is_file():
        errors.append(f"missing {data_path.name}")
    if not csv_path.is_file():
        errors.append(f"missing {csv_path.name}")
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    data = json.loads(data_path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "dataset_sha256",
        "sample_policy",
        "sync_policy",
        "summary",
        "articles",
        "annotations",
    }
    missing = required - set(data)
    if missing:
        errors.append(f"{data_path.name} missing keys: {', '.join(sorted(missing))}")
    ids = [article.get("id") for article in data.get("articles", [])]
    if len(ids) != len(set(ids)):
        errors.append("duplicate article IDs")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != len(ids):
        errors.append(f"{csv_path.name} row count differs from {data_path.name}")
    if {row.get("id") for row in rows} != set(ids):
        errors.append(f"article IDs differ between {csv_path.name} and {data_path.name}")
    for index, annotation in enumerate(data.get("annotations", []), start=1):
        required_annotation = {
            "dimension",
            "label",
            "article_ids",
            "evidence",
            "rule",
            "confidence",
        }
        missing_annotation = required_annotation - set(annotation)
        if missing_annotation:
            errors.append(
                f"annotation {index} missing keys: "
                f"{', '.join(sorted(missing_annotation))}"
            )
        unknown_ids = set(annotation.get("article_ids", [])) - set(ids)
        if unknown_ids:
            errors.append(
                f"annotation {index} references unknown article IDs: "
                f"{', '.join(sorted(unknown_ids))}"
            )

    report = artifact_path(root, "methodology_report")
    framework = artifact_path(root, "copywriting_framework")
    if not args.allow_missing_report:
        if not report.is_file():
            errors.append(f"missing {report.name}")
        elif data["dataset_sha256"] not in report.read_text(encoding="utf-8"):
            errors.append(f"report fingerprint differs from {data_path.name}")
        if not framework.is_file():
            errors.append(f"missing {framework.name}")

    dashboard = artifact_path(root, "dashboard")
    if not args.allow_missing_html:
        if not dashboard.is_file():
            errors.append(f"missing {dashboard.name}")

    sync = artifact_path(root, "lark_sync")
    if sync.exists():
        sync_data = json.loads(sync.read_text(encoding="utf-8"))
        for key in ("doc_token", "url", "title", "content_sha256", "updated_at"):
            if not sync_data.get(key):
                errors.append(f"{sync.name} missing {key}")

    if errors:
        print("validation: failed", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"validation: passed ({len(ids)} articles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
