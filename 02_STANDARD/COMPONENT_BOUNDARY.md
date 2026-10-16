# Component Boundary Standard

## Plane
- `PRODUCT_RUNTIME`: user-facing product execution.
- `DELIVERY`: development, build, test, evidence and release infrastructure.

The same technology can appear in distinct planes, such as a product runtime provider and a release test harness. Do not combine them merely because they share a vendor or technology.

## Component class
- `CORE`: minimal product identity, essential contracts and authoritative kernel.
- `MODULE`: first-party capability required by a declared scope, unless it satisfies the EXTENSION boundary contract below.
- `EXTENSION`: removable/disableable through a published optional boundary, with BASE surviving removal and no Core implementation dependency. This classification takes precedence over MODULE even when a milestone requires the capability; record that requirement in `required_scopes`. BASE must never require an EXTENSION.
- `GENERATED_VIEW`: derived documentation, index or other view from machine SSOT.
- `EXTERNAL`: provider, service or runtime outside the product owner boundary.

## Testable boundaries
1. Core has **zero direct implementation imports** into optional extensions.
2. Removing or disabling all extensions leaves `BASE` operational.
3. Extensions access Core-owned state only through published ports.
4. Prefer public ports instead of direct private cross-extension implementation imports.
5. Built-in distribution does **not** imply Core ownership.
6. Do not make a required Core Module disappear by flipping an optional extension flag.
7. Delivery components do not inherit product-runtime classifications without explicit ownership.

Choose proportional module granularity. Explicit public-contract composition is more important than physical folder symmetry.
