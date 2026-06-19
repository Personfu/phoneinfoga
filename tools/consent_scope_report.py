#!/usr/bin/env python3
"""Build a consent-first phone OSINT report from analyst-provided notes.

No lookup APIs, carrier queries, scraping, or enrichment are performed here. The
script structures evidence that the subject provided or explicitly authorized.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def render(data: dict[str, Any]) -> str:
    subject = data.get('subject_alias', 'authorized subject')
    lines = [
        '# Consent-Scoped Phone OSINT Report',
        '',
        f'- Subject alias: {subject}',
        f'- Consent record: {data.get("consent_record", "TBD")}',
        f'- Scope expiration: {data.get("scope_expiration", "TBD")}',
        '',
        '## Authorized Identifiers',
        '',
    ]
    for item in data.get('identifiers', []):
        lines.append(f'- `{item.get("type", "unknown")}`: `{item.get("value", "redacted")}` — {item.get("source", "provided by subject")}')

    lines.extend(['', '## Findings', ''])
    for finding in data.get('findings', []):
        lines.append(f'- {finding.get("title", "Finding")}: {finding.get("summary", "TBD")}')

    lines.extend([
        '',
        '## Boundary',
        'Do not enrich beyond the explicit consent scope. Do not collect personal data from unrelated parties. Redact raw numbers before publishing.',
        '',
    ])
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Render a consent-scoped OSINT report.')
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(render(json.loads(args.input.read_text(encoding='utf-8'))), encoding='utf-8')
    print(f'wrote {args.output}')


if __name__ == '__main__':
    main()
