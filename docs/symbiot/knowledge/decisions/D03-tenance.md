---
type: Décision
title: D3 — Tenance
description: Rôles PostgreSQL et schémas par application, FalkorDB en graphes nommés, SeaweedFS en buckets, Keycloak en clients, namespaces k3s : le quintuplet de tenance.
tags:
  - tenance
  - stockage
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
impacte:
  - /conventions/tenance.md
  - /conventions/postgresql.md
verified:
  - by: human:vs
    at: 2026-10-16T12:00:00+02:00
---

# D3 — Tenance

**Décision validée le 2026-10-16.** Rôles PostgreSQL et schémas par application, FalkorDB en graphes nommés, SeaweedFS en buckets, Keycloak en clients, namespaces k3s : le quintuplet de tenance.

**Conséquence :** Isolation par rôle, unification par les clés.

**Concepts impactés :**
- [/conventions/tenance.md](/conventions/tenance.md)
- [/conventions/postgresql.md](/conventions/postgresql.md)

**Origine :** [/evaluations/comparatif.md](/evaluations/comparatif.md) §7 et §8, échanges du 16 octobre, [/references/plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md) §0.
