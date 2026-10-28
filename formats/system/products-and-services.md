# Format: system/products-and-services (version 1)

## Purpose

The optional catalog of the discrete products and services the organization operating this application can sell. Each record says what the item is, the specification language that goes onto a customer order form, how it is priced, and how often it recurs. Proposal creation and order forms draw from this catalog. It holds no client business facts.

## Location

`system/products-and-services.md`. One repository-wide registry. The file is optional: when the application sells nothing from a fixed catalog, it is absent, and no check requires it.

## Header

The system header defined in `formats/README.md` with `format: system/products-and-services` and `format_version: 1`. No `client` key.

## Body

When no item is recorded yet, the body is the single line `None`. Otherwise each record uses the item's name as its `#` heading and these `##` sections in order:

```markdown
# Managed Onboarding
## Overview
What the product or service is and who it is for, in a short paragraph.

## Specification
The exact language that is copied unchanged into the order form's `Specification` cell for this item. A single paragraph with no line breaks and no pipe characters, so it fits a table cell.

## Pricing Model
A Display Name from Pricing Models.

## Pricing Unit
What one unit is, such as `per month`, `per seat`, `per report`, or `per project`.

## List Price
The standard price per Pricing Unit, written as a number with its currency code, such as `1500.00 USD`, or `None` when the price is always negotiated.

## Frequency
A Display Name from Frequencies: how often the item recurs or is delivered.

## Status
A Display Name from Item Statuses (`Active` or `Retired`).
```

## Rules

- The `#` heading is the item's name and is its reference key. Order forms cite it exactly.
- Specification language is written once, here, and copied verbatim to order forms. Changing it later does not alter an existing order form.
- A `Retired` item stays in the file and cannot be added to a new order form.
- Never delete an item.
- This file holds no client names, prices negotiated for one client, or other client facts.

## Vocabularies

Pricing Models:

| Display Name | Meaning |
| --- | --- |
| Fixed Fee | One price regardless of volume. |
| Per Unit | Price multiplied by the quantity of the Pricing Unit. |
| Tiered | Price per unit changes by volume band, described in Overview. |
| Usage-Based | Price follows measured consumption of the Pricing Unit. |
| Time and Materials | Price follows time spent plus materials. |

Frequencies:

| Display Name | Meaning |
| --- | --- |
| Daily | Recurs every day. |
| Weekly | Recurs every week. |
| Monthly | Recurs every month. |
| Quarterly | Recurs every quarter. |
| Annual | Recurs every year. |
| One Time | Occurs once. |

Item Statuses:

| Display Name | Meaning |
| --- | --- |
| Active | The item can be added to a new order form. |
| Retired | The item remains for history and cannot be newly sold. |

## Checks

- System header with `format: system/products-and-services` and `format_version: 1`.
- The body is `None`, or every `#` heading is unique and contains `## Overview`, `## Specification`, `## Pricing Model`, `## Pricing Unit`, `## List Price`, `## Frequency`, and `## Status` in that order.
- `## Overview` and `## Specification` are not `None`, and `## Specification` is a single line without a pipe character.
- `## Pricing Model`, `## Frequency`, and `## Status` are Display Names from their vocabularies.
- `## List Price` is `None` or `<number> <ISO 4217 code>`.
