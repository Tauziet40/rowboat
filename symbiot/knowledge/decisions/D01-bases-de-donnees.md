---
type: Décision
title: D1 — Bases de données
description: PostgreSQL pour le relationnel, FalkorDB pour vecteurs et graphe, pas de pgvector ; Cognee comme middleware de peuplement des bases vecteur et graphe pour les frameworks.
tags:
  - stockage
  - mémoire
  - rag
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
impacte:
  - /composants/postgresql.md
  - /composants/falkordb.md
  - /composants/cognee.md
  - /composants/agent-stack.md
  - /composants/centaur.md
verified:
  - by: human:vs
    at: 2026-10-16T12:00:00+02:00
---

# D1 — Bases de données

**Décision validée le 2026-10-16.** PostgreSQL pour le relationnel, FalkorDB pour vecteurs et graphe, pas de pgvector ; Cognee comme middleware de peuplement des bases vecteur et graphe pour les frameworks.

**Conséquence :** Les forks de stockage sont des adaptateurs minces, déjà expérimentés.

**Concepts impactés :**
- [/composants/postgresql.md](/composants/postgresql.md)
- [/composants/falkordb.md](/composants/falkordb.md)
- [/composants/cognee.md](/composants/cognee.md)
- [/composants/agent-stack.md](/composants/agent-stack.md)
- [/composants/centaur.md](/composants/centaur.md)

**Origine :** [/evaluations/comparatif.md](/evaluations/comparatif.md) §7 et §8, échanges du 16 octobre, [/references/plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md) §0.
