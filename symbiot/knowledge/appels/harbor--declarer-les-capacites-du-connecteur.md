---
type: Appel
title: Harbor — Déclarer les capacités du connecteur
description: I4 : POST routes.declareCapabilities
tags:
  - serveur
  - poste
flux: I4
brique: /composants/harbor.md
appel: POST routes.declareCapabilities
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Harbor — Déclarer les capacités du connecteur

| | |
|---|---|
| **Flux** | I4 |
| **Besoin** | Déclarer les capacités du connecteur |
| **Service client** | env.service.declareCapabilities (conductor/connector.ts:452) |
| **Appel** | POST routes.declareCapabilities |
| **Contrat** | `apps/harbor/packages/protocol/src/invocation.ts` ConnectorCapabilities |
| **Fonction servie** | `apps/harbor/packages/server/src/http.ts:336` |
| **Auth** | agent |
| **Événements / statut** | aucun |
| **Test au fil** | `apps/harbor/packages/server/test/option-defaults.test.ts` |

Brique : [/composants/harbor.md](/composants/harbor.md) · Interface : [/interfaces/harbor.md](/interfaces/harbor.md)
