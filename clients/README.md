# Clients — inventory

Each client (or primary business entity) has one isolated folder under `clients/<slug>/`, where `<slug>` is lowercase kebab-case. Every client folder contains `client.md`, `open-items.md`, and `decision-log.md`, and holds `order-form.md` when the client has ordered products or services, all governed by `formats/clients/`.

Use the `setup-client` skill (`/setup-client`) to onboard a new client folder from whatever information you have; it interviews you for the rest. Never create a client folder by hand outside `setup-client`. Use `/client-status <slug>` to see what is in flight for a client, and `/whats-next` to pick up the steps that match your role.

| Client Slug | Name | Status |
| --- | --- | --- |
| `None` | — | — |
