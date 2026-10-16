---
type: Appel
title: BeeAI Framework — Permission d'outil
description: Politique : `AskPermissionRequirement(include=None, *, handler: AskHandler=None, exclude=None, remember_choices=False, hide_disallowed=False, always_all
tags:
  - serveur
  - sandbox
flux: Politique
brique: /composants/beeai-framework.md
generated:
  by: explore-agent/carte-des-appels
  at: 2026-10-16T20:30:00+02:00
status: draft
stale_after: 2027-01-16T00:00:00+02:00
---
# BeeAI Framework — Permission d'outil

| | |
|---|---|
| **Flux** | Politique |
| **Besoin** | Permission d'outil |
| **Service client** | RequirementAgent |
| **Appel** | `AskPermissionRequirement(include=None, *, handler: AskHandler=None, exclude=None, remember_choices=False, hide_disallowed=False, always_allow=False, middlewares=None)` ; `AskHandler = MaybeAsync[[AnyTool, dict], bool]` |
| **Contrat** | `python/beeai_framework/agents/requirement/requirements/ask_permission.py` |
| **Fonction servie** | `:29` ; init :59 s'abonne au start de l'outil (bloquant, match_nested) ; refus → data.output = StringToolOutput(« This tool is not allowed to be used. ») ; handler par défaut io_confirm(..., data=input) :108 |
| **Auth** | dépend du contexte io : Agent Stack = formulaire, A2A = stdin |
| **Événements / statut** | start de l'outil |
| **Test au fil** | aucun dédié |

Brique : [/composants/beeai-framework.md](/composants/beeai-framework.md) · Interface : [/interfaces/beeai-framework.md](/interfaces/beeai-framework.md)
