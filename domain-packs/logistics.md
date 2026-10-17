---
domain: logistics
description: Routing, ETAs, capacity and exception handling for supply chain and delivery problems.
---

# Logistics Pack

1. Disclaimer: planning aid; operational decisions need human sign-off.
2. Units and rules: state units (km, kg, hours), timezone, and cost currency; show formulas for ETA, load factor and cost per unit.
3. Entities: shipments, routes, vehicles, depots, time windows. Output: plan, exceptions, cost/time impact.
4. Grounding: use provided manifests and distance tables; flag any assumed speed or traffic factor as `[ESTIMATE]`.
5. PII: mask driver and customer personal data.
6. Judge Preset: a plan with one overloaded vehicle or one missed time window to fix.
7. Tests: impossible constraints, out-of-scope legal question, malformed manifest.
