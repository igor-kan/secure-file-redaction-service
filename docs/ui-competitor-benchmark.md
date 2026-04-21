# UI Competitor Benchmark

## Competitors Reviewed

- Adobe Acrobat redaction guidance: https://www.adobe.com/acrobat/resources/how-to-redact-a-pdf.html
- Redactable feature set: https://www.redactable.com/features
- CaseGuard platform: https://caseguard.com/

## Key Patterns Observed

- Redaction tooling must make irreversibility clear and auditable.
- Presets/templates accelerate repetitive compliance workflows.
- Teams need structured evidence such as audit trails and action identifiers.

## Implemented Adaptations

- Added redaction presets endpoint and frontend preset selector.
- Added redaction box normalization/validation to reduce malformed redactions.
- Added `audit_id` in redaction responses and surfaced it in the UI.
- Added preset and custom-box controls to mimic production review workflows.
