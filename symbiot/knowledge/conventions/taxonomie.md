---
type: Convention
title: Taxonomie des types et des tags
description: Vocabulaire fermé des types OKF et des tags transversaux du bundle.
tags:
  - okf
  - connaissance
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Taxonomie des types et des tags

**Types** (un répertoire par type) : Composant, Interface, Appel, Décision, Chantier, Convention, Scénario, Provenance, Inventaire, Évaluation, Méthode, Référence (archive d'un plan validé, stable, jamais dépréciée), Vue (générée, non éditée).

**Tags** (vocabulaire fermé, extension par PR sur ce fichier) : poste, serveur, connaissance, identité, secrets, mémoire, rag, okf, mcp, a2a, acp, sandbox, k3s, routage, stockage, tenance, gouvernance, workflows, inspirant, core.

**Règles de confiance** : un concept écrit par un agent naît `draft` sans `verified` et passe `stable` au `verified: human:…` ; `stale_after` obligatoire sur inventaire, provenance, évaluations et tout concept citant une version amont, un trimestre par défaut ; rien ne s'édite rétroactivement, un nouvel arbitrage crée un concept `stable` et passe l'ancien en `deprecated` avec un lien « remplacé par ».
