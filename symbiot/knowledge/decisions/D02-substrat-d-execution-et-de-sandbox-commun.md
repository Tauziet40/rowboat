---
type: Décision
title: D2 — Substrat d'exécution et de sandbox commun
description: k3s pour tous les éléments serveur ; la primitive de sandbox est le CRD Agent Sandbox.
tags:
  - k3s
  - sandbox
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
impacte:
  - /composants/agent-stack.md
  - /composants/centaur.md
  - /composants/dsh.md
verified:
  - by: human:vs
    at: 2026-10-16T12:00:00+02:00
---

# D2 — Substrat d'exécution et de sandbox commun

**Décision validée le 2026-10-16.** k3s pour tous les éléments serveur ; la primitive de sandbox est le CRD Agent Sandbox.

**Conséquence :** Agent Stack et Centaur reviennent en V1 ; DSH tourne en pod.

**Concepts impactés :**
- [/composants/agent-stack.md](/composants/agent-stack.md)
- [/composants/centaur.md](/composants/centaur.md)
- [/composants/dsh.md](/composants/dsh.md)

**Origine :** [/evaluations/comparatif.md](/evaluations/comparatif.md) §7 et §8, échanges du 16 octobre, [/references/plan-methode-deploiement-v1.md](/references/plan-methode-deploiement-v1.md) §0.
