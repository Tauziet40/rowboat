---
type: Appel
title: Cognee — Suivre l'achèvement par polling
description: I2 : MCP `cognify_status(dataset_name)`
tags:
  - serveur
  - poste
  - mcp
flux: I2
brique: /composants/cognee.md
appel: MCP `cognify_status(dataset_name)`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Suivre l'achèvement par polling

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Suivre l'achèvement par polling |
| **Service client** | agent via executeMcpTool |
| **Appel** | MCP `cognify_status(dataset_name)` |
| **Contrat** | `cognee-mcp/src/server.py:899` cognify_status → cognee_client.py:517 list_datasets (GET /api/v1/datasets/) puis :476 get_pipeline_status (GET /api/v1/datasets/status?dataset=…&pipeline_name=…) |
| **Fonction servie** | `cognee/cognee/api/v1/datasets/routers/get_datasets_router.py:565` get_dataset_status → `cognee/cognee/modules/pipelines/operations/get_pipeline_status.py:6` |
| **Auth** | idem |
| **Événements / statut** | PipelineRunStatus : initiated, started, completed, errored ; plus erreurs des tâches en arrière-plan |
| **Test au fil** | `cognee/cognee/tests/unit/api/test_dataset_processing_status_router.py` |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
