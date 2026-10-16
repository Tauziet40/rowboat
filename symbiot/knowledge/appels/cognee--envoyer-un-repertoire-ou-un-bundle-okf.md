---
type: Appel
title: Cognee — Envoyer un répertoire ou un bundle OKF
description: I2 : REST POST /api/v1/remember multipart `data[]`, `datasetName`/`datasetId`, `run_in_background`, `ontology_key[]` ; `raw_data` = chemin serveur seulement si ACCEPT_LOCAL_FILE_PATH
tags:
  - serveur
  - poste
flux: I2
brique: /composants/cognee.md
appel: REST POST /api/v1/remember multipart `data[]`, `datasetName`/`datasetId`, `run_in_background`, `ontology_key[]` ; `raw_data` = chemin serveur seulement si ACCEPT_LOCAL_FILE_PATH
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:00:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# Cognee — Envoyer un répertoire ou un bundle OKF

| | |
|---|---|
| **Flux** | I2 |
| **Besoin** | Envoyer un répertoire ou un bundle OKF |
| **Service client** | Rowboat doit itérer fichier par fichier en MCP, ou appeler REST directement |
| **Appel** | REST POST /api/v1/remember multipart `data[]`, `datasetName`/`datasetId`, `run_in_background`, `ontology_key[]` ; `raw_data` = chemin serveur seulement si ACCEPT_LOCAL_FILE_PATH |
| **Contrat** | `cognee/cognee/api/v1/remember/routers/get_remember_router.py:119-240` |
| **Fonction servie** | remember.py:887 |
| **Auth** | JWT Bearer, cookie ou X-Api-Key |
| **Événements / statut** | statut renvoyé, puis cognify_status |
| **Test au fil** | idem ci-dessus |

**Note de frontière :** **Lacune** : en MCP un chemin de répertoire est envoyé comme texte (test_mcp_server_hardening.py:252). Aucune notion OKF dans Cognee : le convertisseur du chantier 03 doit produire des fichiers et les envoyer un à un ou par REST multipart.

Brique : [/composants/cognee.md](/composants/cognee.md) · Interface : [/interfaces/cognee.md](/interfaces/cognee.md)
