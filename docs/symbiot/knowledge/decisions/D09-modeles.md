---
type: Décision
title: D9 — Modèles
description: Le proxy serveur (Agent Stack) est l'autorité de routage et de quota, GPU publié au cluster ; le routeur client ne décide qu'en local ou hors ligne.
tags:
  - routage
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
impacte:
  - /composants/proxy-llm.md
  - /chantiers/07-routeur-llm-client.md
  - /chantiers/18-routeur-llm-serveur.md
verified:
  - by: human:vs
    at: 2026-10-16T12:00:00+02:00
---

# D9 — Modèles

**Décision validée le 2026-10-16.** Le proxy serveur (Agent Stack) est l'autorité de routage et de quota, GPU publié au cluster ; le routeur client ne décide qu'en local ou hors ligne.

**Concepts impactés :**
- [/composants/proxy-llm.md](/composants/proxy-llm.md)
- [/chantiers/07-routeur-llm-client.md](/chantiers/07-routeur-llm-client.md)
- [/chantiers/18-routeur-llm-serveur.md](/chantiers/18-routeur-llm-serveur.md)

**Origine :** [/evaluations/comparatif.md](/evaluations/comparatif.md) §7 et §8, échanges du 16 octobre, [/references/plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md) §0.
