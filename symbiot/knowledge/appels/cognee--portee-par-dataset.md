---
type: Appel
title: Cognee — Portée par dataset
description: I5 : `dataset_name` / `datasets` ; défaut `<client>_memory` ou `main_dataset`
tags:
  - serveur
  - poste
flux: I5
brique: /composants/cognee.md
appel: `dataset_name` / `datasets` ; défaut `<client>_memory` ou `main_dataset`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Portée par dataset

| | |
|---|---|
| **Flux** | I5 |
| **Besoin** | Portée par dataset |
| **Service client** | paramètre d'outil |
| **Appel** | `dataset_name` / `datasets` ; défaut `<client>_memory` ou `main_dataset` |
| **Contrat** | `cognee-mcp/src/server.py:1013` _agent_scoped_default_dataset |
| **Fonction servie** | `cognee/cognee/modules/pipelines/layers/resolve_authorized_user_datasets.py:14` |
| **Auth** | — |
| **Événements / statut** | — |
| **Test au fil** | aucun (MCP) |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
