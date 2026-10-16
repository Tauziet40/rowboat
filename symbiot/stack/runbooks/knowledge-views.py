#!/usr/bin/env python3
"""symbiot knowledge views — régénère knowledge/vues/ (par type, tag, statut). Usage: python3 -I knowledge-views.py <bundle>"""
import os, re, sys, datetime
K = sys.argv[1] if len(sys.argv) > 1 else 'knowledge'; TODAY = datetime.date.today().isoformat()
ALL = []
for root, _, files in os.walk(K):
    if os.path.basename(root) == 'vues': continue
    for f in files:
        if not f.endswith('.md') or f in ('index.md', 'log.md'): continue
        s = open(os.path.join(root, f), encoding='utf-8').read()
        if not s.startswith('---'): continue
        fm = s.split('---', 2)[1]; d = {'path': '/' + os.path.relpath(os.path.join(root, f), K)}
        for k in ('type', 'title', 'status'):
            m = re.search(rf'^{k}: (.*)$', fm, re.M); d[k] = m.group(1) if m else '?'
        tags = re.search(r'^tags:\n((?:  - .*\n)+)', fm, re.M); d['tags'] = [t.strip()[2:] for t in tags.group(1).splitlines()] if tags else ['(sans tag)']
        ALL.append(d)
os.makedirs(f'{K}/vues', exist_ok=True)
def vue(name, title, keyf):
    groups = {}
    for d in ALL:
        ks = keyf(d); ks = ks if isinstance(ks, list) else [ks]
        for k in ks: groups.setdefault(k, []).append(d)
    out = [f'---\ntype: Vue\ntitle: {title}\ndescription: Index généré par symbiot knowledge views ; ne pas éditer à la main.\ntags:\n  - okf\ngenerated:\n  by: process:knowledge-views\n  at: {TODAY}T00:00:00+00:00\nstatus: stable\n---\n', f'# {title}\n', f'_Généré le {TODAY}._\n']
    for k in sorted(groups):
        out.append(f'\n## {k}\n'); out += [f"- [{d['title']}]({d['path']})" for d in sorted(groups[k], key=lambda x: x['path'])]
    open(f'{K}/vues/{name}.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
vue('par-type', 'Vue par type', lambda d: d['type']); vue('par-tag', 'Vue par tag', lambda d: d['tags']); vue('par-statut', 'Vue par statut', lambda d: d['status'])
open(f'{K}/vues/index.md', 'w', encoding='utf-8').write('# Vues générées\n\n- [par type](par-type.md)\n- [par tag](par-tag.md)\n- [par statut](par-statut.md)\n')
print(f'{len(ALL)} concepts, 3 vues')
