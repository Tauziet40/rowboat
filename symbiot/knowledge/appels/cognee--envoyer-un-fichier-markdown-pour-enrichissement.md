---
type: Appel
title: Cognee — Envoyer un fichier Markdown pour enrichissement
description: I2 : MCP `remember(filename, content_base64 ≤ 10 Mo, dataset_name, background=true, ontology_key?, custom_prompt?)`
tags:
  - serveur
  - poste
  - mcp
flux: I2
brique: /composants/cognee.md
appel: MCP `remember(filename, content_base64 ≤ 10 Mo, dataset_name, background=true, ontology_key?, custom_prompt?)`
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Envoyer un fichier Markdown pour enrichissement

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Envoyer un fichier Markdown pour enrichissement |
| **Service client** | agent via executeMcpTool |
| **Appel** | MCP `remember(filename, content_base64 ≤ 10 Mo, dataset_name, background=true, ontology_key?, custom_prompt?)` |
| **Contrat** | `cognee-mcp/src/server.py:357` remember → `cognee-mcp/src/cognee_client.py:605` → POST /api/v1/remember (multipart) |
| **Fonction servie** | `cognee/cognee/api/v1/remember/routers/get_remember_router.py:119` remember → `cognee/cognee/api/v1/remember/remember.py:887` (add + cognify + improve) |
| **Auth** | cognee-mcp → API : `_get_headers` cognee_client.py:127, Bearer ou X-Api-Key + X-Tenant-Id |
| **Événements / statut** | background=true renvoie immédiatement ; erreurs dans `_task_errors` (server.py:131) ; suivi par cognify_status |
| **Test au fil** | `cognee-mcp/tests/test_mcp_server_hardening.py:273` ; `cognee/cognee/tests/unit/api/v1/remember/test_remember_router_self_improvement.py` |

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
