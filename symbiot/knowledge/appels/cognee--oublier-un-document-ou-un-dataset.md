---
type: Appel
title: Cognee — Oublier un document ou un dataset
description: I5 : MCP `forget(data_id + dataset | dataset_id, ou dataset, ou everything)`
tags:
  - serveur
  - poste
  - mcp
flux: I5
brique: /composants/cognee.md
appel: MCP `forget(data_id + dataset \| dataset_id, ou dataset, ou everything)`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Oublier un document ou un dataset

| | |
|---|---|
| **Flux** | I5 |
| **Besoin** | Oublier un document ou un dataset |
| **Service client** | agent via executeMcpTool |
| **Appel** | MCP `forget(data_id + dataset | dataset_id, ou dataset, ou everything)` |
| **Contrat** | `cognee-mcp/src/server.py:714` forget → cognee_client.py:884 → POST /api/v1/forget (data_id, dataset, dataset_id, everything, memory_only) |
| **Fonction servie** | `cognee/cognee/api/v1/forget/routers/get_forget_router.py:69` forget_endpoint → `cognee/cognee/api/v1/forget/forget.py:22` |
| **Auth** | permission delete |
| **Événements / statut** | synchrone ; variante REST DELETE /api/v1/datasets/{id}/data/{data_id} (get_datasets_router.py:302) |
| **Test au fil** | `cognee/cognee/tests/unit/api/v1/forget/test_forget_endpoint.py`, test_forget_dataset_args.py, test_forget_memory_only.py ; `cognee/cognee/tests/test_delete_permission.py` |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
