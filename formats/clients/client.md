# Format: clients/client (version 3)

## Purpose

The authoritative record for one client or primary business entity: who they are, and the business context every workflow for them is grounded in. It is the first file an agent reads in `clients/<slug>/`, and no other document in the folder restates its values.

## Location

`clients/<slug>/client.md`. The format identifier is `clients/client`.

## Header

The client header defined in `formats/README.md` with `format: clients/client`, `format_version: 3`, and `client` equal to the folder slug.

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

# Notes
Approval rules, exclusions, and anything negotiated for this client that does not belong in another section, or in `order-form.md`. Write `None` when there is nothing to record.
```

## Rules

- `client.md` is the single authority for client identity inside `clients/<slug>/`. What the client is owed, and when, lives in `order-form.md`.
- Contact details appear only here and in `order-form.md`, never in other documents.
- Payment card or bank numbers must never appear in `client.md`.
- Any section left `None` during onboarding must have a matching open row in `clients/<slug>/open-issues.md`.
- `setup-application` and `improve-process` may extend this format with domain-specific sections by bumping `format_version` and updating `scripts/check.py`.

## Vocabularies

None in the base format. Domain-specific vocabularies are added when `setup-application` customizes the repository.

## Checks

- Client header with `format: clients/client`, `format_version: 3`, and `client` matching the parent folder name.
- All five `#` sections (`# General Information`, `# Business Overview`, `# Business Problem`, `# Solution`, `# Notes`) and their `##` subsections are present in exact order.
- `## Contact` holds two bullets (`- Name: ...` and `- Email: ...`) with a valid email address, or `None` when tracked as an open issue.
- `## Engagement Started` is `YYYY-MM-DD` or `None`.
