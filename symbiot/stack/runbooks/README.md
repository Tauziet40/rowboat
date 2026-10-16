# runbooks `symbiot <action>`

Liste et retours arrière dans `knowledge/methode/deploiement-v1.md`, annexe E. Disponibles aujourd'hui :

| Runbook | Script | Effet |
|---|---|---|
| `symbiot lint` | `knowledge-lint.py` | conformité OKF et règles de projet du bundle |
| `symbiot knowledge views` | `knowledge-views.py` | régénère `knowledge/vues/` |

À écrire : `cluster up`, `tenancy apply`, `deploy`, `backup`, `restore`, `fork sync`, `slice`, `test`, `verify`, `knowledge ingest`, `inventory`, `secrets rotate`.

Exécution : `python3 -I stack/runbooks/knowledge-lint.py knowledge/`
