---
type: Décision
title: D11 — Flux d'événements et versions
description: Le journal append-only de Harbor est le flux canonique ; aucun bus supplémentaire ; versions de Harbor et DSH épinglées.
tags:
  - serveur
  - core
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
impacte:
  - /composants/harbor.md
  - /composants/dsh.md
verified:
  - by: human:vs
    at: 2026-10-16T12:00:00+02:00
---

# D11 — Flux d'événements et versions

**Décision validée le 2026-10-16.** Le journal append-only de Harbor est le flux canonique ; aucun bus supplémentaire ; versions de Harbor et DSH épinglées.

**Concepts impactés :**
- [/composants/harbor.md](/composants/harbor.md)
- [/composants/dsh.md](/composants/dsh.md)

**Origine :** [/evaluations/comparatif.md](/evaluations/comparatif.md) §7 et §8, échanges du 16 octobre, [/references/plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md) §0.
