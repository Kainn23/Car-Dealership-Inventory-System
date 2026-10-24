# Car Dealership Inventory System

A full-stack car dealership inventory application built with FastAPI, PostgreSQL, React, and Tailwind CSS, developed strictly test-first (TDD).

## Architectural Decisions (D1–D6)
- **D1 (Write Permissions):** Vehicle creation (`POST`) and update (`PUT`) are restricted to `admin` users.
- **D2 (Inventory Visibility):** `GET /api/vehicles` returns all vehicles including zero-quantity items to allow the UI to show a disabled "Sold Out" state.
- **D3 (Admin Creation):** Registration `/api/auth/register` creates `user` roles only. Admins are created exclusively through seed scripts / environment bootstrapping.
- **D4 (Price Representation):** Stored as integer cents in PostgreSQL; exposed as formatted decimals via the API.
- **D5 (Purchasing Logic):** Purchases default to 1 unit with an optional quantity parameter (max 10).
- **D6 (Quantity Protection):** `PUT /api/vehicles/:id` explicitly ignores/rejects quantity edits to prevent overwriting concurrent stock decrements.

## My AI Usage
*Detailed reflection and tooling logs will be documented here as development progresses.*
