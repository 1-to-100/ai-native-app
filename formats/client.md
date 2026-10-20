# Format: client (version 1)

## Purpose

The authoritative record for one client or primary business entity in the application: who they are, the business context every workflow for them is grounded in, and their commercial entitlements. It is the first file an agent reads in `clients/<slug>/`, and no other document in the folder restates its values.

## Location

`clients/<slug>/client.md`

## Header

The standard YAML header defined in `formats/README.md` with `format: client`, `format_version: 1`, and `client: <slug>`.

## Body

```markdown
# General Information
## Name
The client's public name, written as they use it.

## Organization
The company or organization name, or `None` when not applicable.

## Website
The client's primary website as a full `https://` URL, or `None` when they do not have one.

## Time Zone
The IANA time zone the client operates in, such as `America/New_York` or `America/Los_Angeles`.

## Engagement Started
The date the engagement began, written `YYYY-MM-DD`, or `None` if not yet started.

## Contact
The primary point of contact as exactly two bullets in this order: `- Name: ...` and `- Email: ...`.

# Business Overview
Who the client is, what they do, who they serve, and the goals of this engagement, grounded in their own words. Write `None` when not yet captured (with a matching row in `open-issues.md`).

# Business Problem
The core problem this client is solving or hired us to address, in their own terms. Write `None` when not yet captured.

# Solution
How the client or engagement addresses that problem. Write `None` when not yet captured.

# Entitlements
## Order Form
Either `order-form.pdf` (when a signed commercial contract is stored in `clients/<slug>/order-form.pdf` with payment details redacted) or `None` (when the application does not require a commercial order form or it is tracked as an open issue).

## Plan Name
The commercial package or tier name, or `None`.

## Starts
The first month the engagement covers (`YYYY-MM`), or `None`.

## Renews
The next renewal or review date (`YYYY-MM-DD`), or `None`.

## Deliverables
A Markdown table of recurring or scoped deliverables owed to the client, or `None` when none are defined.

| Deliverable | Quantity | Cadence | Notes |
| --- | --- | --- | --- |

# Notes
Commercial overrides, approval rules, exclusions, and anything negotiated for this client that does not belong in another section. Write `None` when there is nothing to record.
```

## Rules

- `client.md` is the single authority for client identity and entitlements inside `clients/<slug>/`.
- Contact details appear only here (and on `order-form.pdf` if present), never in other documents.
- Payment card or bank numbers must never appear in `client.md` or `order-form.pdf`.
- Any section left `None` during onboarding must have a matching open row in `clients/<slug>/open-issues.md`.
- `create-application` and `improve-process` may extend this format with domain-specific sections by bumping `format_version` and updating `scripts/check.py`.

## Vocabularies

None in the base format; domain-specific vocabularies are added when `create-application` customizes the repository.

## Checks

- Standard header with `format: client`, `format_version: 1`, and `client` matching the parent folder name.
- All six `#` sections (`# General Information`, `# Business Overview`, `# Business Problem`, `# Solution`, `# Entitlements`, `# Notes`) and their `##` subsections are present in exact order.
- `## Contact` holds two bullets (`- Name: ...` and `- Email: ...`) with a valid email address, or `None` when tracked as an open issue.
- `## Engagement Started` and `## Renews` are `YYYY-MM-DD` or `None`; `## Starts` is `YYYY-MM` or `None`.
- If `## Order Form` is `order-form.pdf`, that file exists in `clients/<slug>/order-form.pdf`.
