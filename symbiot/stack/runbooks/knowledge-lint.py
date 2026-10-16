#!/usr/bin/env python3
"""symbiot lint — conformité OKF 0.2 et règles de projet du bundle (knowledge/conventions/derivation.md).
Usage: python3 -I knowledge-lint.py <chemin du bundle>
Règles : frontmatter et type sur tout concept ; index.md sans frontmatter (sauf racine) ; liens résolus ;
lien vers un concept deprecated sans note « remplacé par » ; stale_after dépassé ; generated.at après le
dernier verified d'un concept stable ; brique (Composant) sans degré déclaré.
"""
import os, re, sys, datetime
K = sys.argv[1] if len(sys.argv) > 1 else 'knowledge'
errs = []
def fm_of(s):
    if not s.startswith('---'): return None
    return s.split('---', 2)[1]
status = {}
for root, _, files in os.walk(K):
    for f in files:
        if not f.endswith('.md'): continue
        p = os.path.join(root, f); s = open(p, encoding='utf-8').read(); rel = '/' + os.path.relpath(p, K)
        fm = fm_of(s)
        if f == 'index.md':
            if fm is not None and rel != '/index.md': errs.append(f'{rel}: index.md avec frontmatter')
            continue
        if f == 'log.md': continue
        if fm is None: errs.append(f'{rel}: frontmatter absent'); continue
        t = re.search(r'^type: (\S.*)$', fm, re.M)
        if not t: errs.append(f'{rel}: type manquant'); continue
        st = re.search(r'^status: (\S+)', fm, re.M); st = st.group(1) if st else 'stable'
        status[rel] = st
        if t.group(1).strip() == 'Composant' and not re.search(r'^degre:', fm, re.M): errs.append(f'{rel}: composant sans degré')
        sa = re.search(r'^stale_after: (\S+)', fm, re.M)
        if sa:
            try:
                if datetime.datetime.fromisoformat(sa.group(1)) < datetime.datetime.now(datetime.timezone.utc): errs.append(f'{rel}: stale_after dépassé')
            except ValueError: errs.append(f'{rel}: stale_after invalide')
        if st == 'stable':
            g = re.search(r'^generated:\n(?:  .*\n)*?  at: (\S+)', fm, re.M); v = re.findall(r'^  (?:- )?at: (\S+)', fm.split('verified:')[1], re.M) if 'verified:' in fm else []
            if g and v and max(v) < g.group(1): errs.append(f'{rel}: generated.at postérieur au dernier verified')
for root, _, files in os.walk(K):
    for f in files:
        if not f.endswith('.md'): continue
        p = os.path.join(root, f); s = open(p, encoding='utf-8').read(); rel = '/' + os.path.relpath(p, K)
        for l in re.findall(r'\]\(([^)#\s]+?)(?:#[^)]*)?\)', s):
            if l.startswith(('http', 'mailto')) or '/deprecated/' in l: continue
            tgt = os.path.normpath(os.path.join(K, l.lstrip('/')) if l.startswith('/') else os.path.join(root, l))
            if not os.path.exists(tgt): errs.append(f'{rel}: lien non résolu {l}'); continue
            trel = '/' + os.path.relpath(tgt, K)
            if status.get(trel) == 'deprecated' and status.get(rel) != 'deprecated' and 'remplacé par' not in s: errs.append(f'{rel}: lien vers deprecated {trel} sans note « remplacé par »')
print(f'{len(errs)} erreur(s)'); print('\n'.join(errs)); sys.exit(1 if errs else 0)
