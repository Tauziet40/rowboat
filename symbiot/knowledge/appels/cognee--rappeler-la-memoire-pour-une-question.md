---
type: Appel
title: Cognee — Rappeler la mémoire pour une question
description: I5 : MCP `recall(query, datasets="a,b", search_type?, top_k?, session_id?)`
tags:
  - serveur
  - poste
  - mcp
flux: I5
brique: /composants/cognee.md
appel: MCP `recall(query, datasets="a,b", search_type?, top_k?, session_id?)`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Rappeler la mémoire pour une question

| | |
|---|---|
| **Flux** | I5 |
| **Besoin** | Rappeler la mémoire pour une question |
| **Service client** | agent via executeMcpTool |
| **Appel** | MCP `recall(query, datasets="a,b", search_type?, top_k?, session_id?)` |
| **Contrat** | `cognee-mcp/src/server.py:531` recall → cognee_client.py:824 → POST /api/v1/recall (query, datasets, dataset_ids, search_type, top_k=15, only_context, session_id) |
| **Fonction servie** | `cognee/cognee/api/v1/recall/routers/get_recall_router.py:213` recall → `cognee/cognee/api/v1/recall/recall.py:349` |
| **Auth** | idem ; résultats filtrés aux datasets lisibles par l'utilisateur |
| **Événements / statut** | résultat vide → diagnostic get_recall_state (cognee_client.py:763 → /datasets/status/progress), signale une ingestion en cours |
| **Test au fil** | `cognee/cognee/tests/unit/api/recall/*.py`, test_query_required_on_recall_and_search.py ; `cognee-mcp/tests/test_recall_summary.py` |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
