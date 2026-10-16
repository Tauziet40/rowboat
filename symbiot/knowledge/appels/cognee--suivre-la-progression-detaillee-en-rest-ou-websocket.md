---
type: Appel
title: Cognee — Suivre la progression détaillée en REST ou WebSocket
description: I2 : GET /api/v1/datasets/status/progress ; GET /api/v1/datasets/{id}/processing-status ; WS /api/v1/cognify/subscribe/{pipeline_run_id}
tags:
  - serveur
  - poste
flux: I2
brique: /composants/cognee.md
appel: GET /api/v1/datasets/status/progress ; GET /api/v1/datasets/{id}/processing-status ; WS /api/v1/cognify/subscribe/{pipeline_run_id}
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Suivre la progression détaillée en REST ou WebSocket

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Suivre la progression détaillée en REST ou WebSocket |
| **Service client** | client HTTP |
| **Appel** | GET /api/v1/datasets/status/progress ; GET /api/v1/datasets/{id}/processing-status ; WS /api/v1/cognify/subscribe/{pipeline_run_id} |
| **Contrat** | get_datasets_router.py:646 get_dataset_progress, :994 get_dataset_processing_status ; `cognee/cognee/api/v1/cognify/routers/get_cognify_router.py:312` subscribe_to_cognify_info |
| **Fonction servie** | module pipelines |
| **Auth** | WS : `?token=` accepté |
| **Événements / statut** | flux poussé toutes les 2 s, fermé à la fin du pipeline |
| **Test au fil** | `cognee/cognee/tests/unit/api/test_status_progress_router.py`, test_cognify_subscribe_auth.py |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
