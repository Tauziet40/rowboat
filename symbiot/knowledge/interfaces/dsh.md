---
type: Interface
title: DSH — ACP, SDK JSON-RPC, client MCP, politique, credentials
description: Surfaces par lesquelles un client pilote DSH et par lesquelles DSH consomme Cognee, est gouverné et résout ses secrets.
tags:
  - serveur
  - poste
  - acp
  - mcp
  - sandbox
  - gouvernance
  - secrets
protocole: ACP v1 stdio ; JSON-RPC stdio ; Cordis config
auth: aucune sur ACP et SDK ; headers ou env statiques vers les MCP
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# DSH — ACP, SDK JSON-RPC, client MCP, politique, credentials

Appels dans [/appels/](/appels/index.md), préfixe `dsh--`. Vérification des seams : [/evaluations/dsh-seams.md](/evaluations/dsh-seams.md). Remarques : ACP refuse le transport MCP `sse` ; le SDK n'a que trois méthodes et aucune requête serveur → client, donc les approbations y sont refusées ; aucune authentification sur ACP.
