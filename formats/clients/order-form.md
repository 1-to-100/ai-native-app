# Format: clients/order-form (version 1)

## Purpose

The record of what one client has ordered: the products and services owed, their specification language, quantities, prices, and frequency, plus the term and commercial terms around them. It is the single authority for what is owed to the client and when. Skills that check delivery conformance read this file directly and compare the delivery schedule to its `# Line Items`.

## Location

`clients/<slug>/order-form.md`. Optional: a client with no commercial order has none. The format identifier is `clients/order-form`.

## Header

The client header defined in `formats/README.md` with `format: clients/order-form`, `format_version: 1`, and `client` equal to the folder slug.

## Body

```markdown
# Order Details
## Order Number
The order's identifier, such as `OF-0001`, or `None`.

## Status
A Display Name from Order Statuses.

## Plan Name
The commercial package or tier name, or `None`.

## Order Date
The date the order was drafted, `YYYY-MM-DD`.

## Effective Date
The date the order takes effect, `YYYY-MM-DD`, or `None`.

## Term End
The date the current term ends, `YYYY-MM-DD`, or `None`.

## Renewal
A Display Name from Renewal Terms.

# Parties
## Customer Legal Name
The legal name of the ordering customer, or `None`.

## Customer Signatory
Exactly two bullets, `- Name: ...` and `- Email: ...`, or `None`.

## Sales Representative
The email heading of the user in `system/users.md` who sold the order, or `None`.

# Line Items
`None`, or a Markdown table, one row per product or service owed.

| Product or Service | Specification | Quantity | Unit | Unit Price | Frequency |
| --- | --- | --- | --- | --- | --- |

# Commercial Terms
## Currency
The ISO 4217 currency code, or `None`.

## Billing Contact
Exactly two bullets, `- Name: ...` and `- Email: ...`, or `None`.

## Payment Terms
The agreed payment terms in the customer's words, such as `Net 30`, or `None`.

## Discounts and Adjustments
Any negotiated discount, credit, or adjustment, or `None`.

# Execution
## Signed Date
The date the customer signed, `YYYY-MM-DD`, or `None` until signed.

## Signed Copy
`order-form.pdf` when a signed copy is stored beside this file with payment details redacted, or `None`.

# Notes
Anything negotiated or agreed that does not belong in another section. `None` when there is nothing to record.
```

## Rules

- `Product or Service` is the exact name of an item in `system/products-and-services.md` when that catalog exists. `Specification` is that item's `Specification` copied verbatim. `Unit` is its Pricing Unit. `Frequency` is the agreed frequency, which may differ from the catalog default.
- `Quantity` is a positive number or `None`. `Unit Price` is a number or `None`, in the order's Currency.
- This file is the only place in the client folder that states what is owed and how often. Other documents do not restate it.
- Contact details appear only here and in `client.md`, never in other documents.
- Payment card or bank numbers must never appear here or in `order-form.pdf`.
- Do not invent a price, term, or quantity. Write `None` and open an issue in `open-issues.md` with Area `Order Form`.
- A `Signed` order is not edited to change what was agreed. An amendment is recorded as a decision in `decision-log.md` and then applied to this file, with the prior text kept in Git history.

## Vocabularies

Order Statuses:

| Display Name | Meaning |
| --- | --- |
| Draft | Being prepared; not yet sent. |
| Sent | Sent to the customer for signature. |
| Signed | Signed by the customer and in force. |
| Cancelled | Withdrawn or ended; remains for history. |

Renewal Terms:

| Display Name | Meaning |
| --- | --- |
| Auto-Renew | Renews at term end unless cancelled. |
| Manual Renewal | Renews only by a new agreement. |
| Does Not Renew | Ends at term end. |

Frequencies are defined in `formats/system/products-and-services.md`.

## Checks

- Client header with `format: clients/order-form`, `format_version: 1`, and `client` matching the parent folder name.
- All six `#` sections (`# Order Details`, `# Parties`, `# Line Items`, `# Commercial Terms`, `# Execution`, `# Notes`) and their `##` subsections are present in exact order.
- `## Status` and `## Renewal` are Display Names from their vocabularies. `## Order Date`, `## Effective Date`, `## Term End`, and `## Signed Date` are `YYYY-MM-DD` (the last three may be `None`).
- Contact sections hold two bullets with a valid email, or `None`. `## Sales Representative` is `None` or resolves to a user in `system/users.md`.
- `# Line Items` is `None` or a table with the exact columns above and a `Frequency` Display Name in every row.
- When `system/products-and-services.md` exists, every `Product or Service` resolves to an item in it and every `Specification` equals that item's `Specification`.
- A `Signed` order has a `Signed Date`. If `## Signed Copy` is `order-form.pdf`, that file exists beside this file.
- No row or section contains a card or bank number.
