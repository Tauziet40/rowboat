---
type: Convention
title: Convention PostgreSQL
description: Une base, un schéma et un rôle par application, migration par outil amont dans son schéma, sauvegarde par schéma.
tags:
  - stockage
  - tenance
generated:
  by: claude-fable-5.1/session-01MK6
  at: 2026-10-16T18:00:00+02:00
status: stable
stale_after: 2027-01-16T00:00:00+02:00
---

# Convention PostgreSQL

- Une instance, une base, **un schéma et un rôle par application** ; le rôle est propriétaire de son seul schéma.
- Migrations : Alembic (Agent Stack, Cognee), `migrations.ts` (Harbor), sqlx (Centaur), chacun avec `search_path` sur son schéma ; les extensions se posent au niveau base ; pas de pgvector (D1).
- Sauvegarde et restauration par schéma (`pg_dump -n`), runbook `symbiot backup`.
- Point à consigner : Cognee avec `ENABLE_BACKEND_ACCESS_CONTROL=true` isole chaque couple utilisateur et dataset dans sa propre base ; le choix de l'installation existante fixe la convention (D8).
